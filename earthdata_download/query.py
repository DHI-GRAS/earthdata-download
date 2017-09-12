import json
import logging
import datetime

import requests

logger = logging.getLogger('earthdata_download.query')

nasa_echo_url_base = 'https://api.echo.nasa.gov/catalog-rest/echo_catalog/granules.json?page_num=1'
max_n_products = 2000


def url_from_query(short_name='', version='', date_range=(), extent={}, n_products=max_n_products):
    """Generate EarthData query url for given parameters

    Parameters
    ----------
    short_name : str
        product short name
    version : str
        product version (e.g. '005', leading zeros matter!)
    date_range : (datetime.datetime, datetime.datetime)
        date range
    extent : dict
        extent dictionary
        must have entries xmin, xmax, ymin, ymax
    n_products : int (max max_n_products)
        number of products to retrieve

    Details
    -------
    https://wiki.earthdata.nasa.gov/display/echo/ECHO+REST+Search+Guide
    """
    url = nasa_echo_url_base

    if n_products > max_n_products:
        raise ValueError(
                'Currently, the API only allows for {} products at a time'
                ''.format(max_n_products))
    url += '&page_size={}'.format(n_products)

    if short_name:
        url += '&short_name={}'.format(short_name)

    if version:
        url += '&version={}'.format(version)

    if date_range:
        datefmt = '%Y-%m-%dT%H:%M:%S'
        start_date, end_date = _get_dates(date_range)
        url += '&temporal[]={},{}'.format(*[d.strftime(datefmt) for d in (start_date, end_date)])

    if extent:
        url += '&bounding_box={xmin},{ymin},{xmax},{ymax}'.format(**extent)

    return url


def get_entries_from_url(url):
    """Get entries from query url

    Parameters
    ----------
    url : str
        REST query url
    """
    r = requests.get(url)

    catalogue = json.loads(r.text)
    try:
        entries = catalogue['feed']['entry']
    except KeyError:
        raise ValueError('Query with url \'{}\' did not return any files. '
                'Catalogue:\n\n{}'.format(url, catalogue.__repr__()))
    return entries


def get_data_urls_from_entries(entries, linkno=0):
    """Get data URLS from entries

    Parameters
    ----------
    entries : list of dict
        entries from JSON response
    linkno : int
        number of link to get
    """
    all_href = [e['links'][linkno]['href'] for e in entries]
    return [url for url in all_href if not url.endswith('.jpg')]


def get_data_urls(url, linkno=0):
    """Get data urls from query url

    Parameters
    ----------
    url : str
        REST query url
    """
    entries = get_entries_from_url(url)
    return get_data_urls_from_entries(entries, linkno=linkno)


def date_from_timestamp(s):
    # 2000-02-18T00:00:00.000Z
    return datetime.datetime.strptime(s[:10], '%Y-%m-%d')


def get_entry_start_date(e):
    """Returns start date for entry"""
    return date_from_timestamp(e['time_start'])


def get_entry_end_date(e):
    """Returns end date for entry"""
    return date_from_timestamp(e['time_end'])


def find_data(short_name='', version='', start_date=None, end_date=None, extent={}, linkno=0):
    """Query EarthData for products and return download urls

    Parameters
    ----------
    short_name : str
        product short name
    version : str
        product version (e.g. '005', leading zeros matter!)
    date_range : (datetime.datetime, datetime.datetime)
        date range
        at least one must be specified
    extent : dict
        extent dictionary
        must have entries xmin, xmax, ymin, ymax
    linkno : int
        number of link to get
        different products have different links
        e.g. opendap etc.
        0 is usually a good download link
    """
    if start_date is None:
        # retrieve first avaliable product date
        url = url_from_query(
                short_name=short_name, version=version,
                date_range=(), extent=extent, n_products=1)

        e = get_entries_from_url(url)[0]
        start_date = get_entry_start_date(e)

    if end_date is None:
        # use today as latest date
        end_date = datetime.datetime.now()

    # iterate until the full query period has been retrieved
    date_range = (start_date, end_date)
    data_urls = []
    while True:
        url = url_from_query(
                short_name=short_name, version=version,
                date_range=date_range, extent=extent,
                n_products=max_n_products)
        logger.debug('Query URL is \'{}\'.'.format(url))
        try:
            entries = get_entries_from_url(url)
        except ValueError:
            # no entries found
            break
        data_urls += get_data_urls_from_entries(entries, linkno=linkno)

        # check if there is more
        if len(entries) < max_n_products:
            # nope
            break

        # check if the end date was reached
        last_end_date = get_entry_end_date(entries[-1])
        if last_end_date >= end_date:
            # yes
            break

        # make another query starting from last date of results
        dt = datetime.timedelta(seconds=1)
        date_range = (last_end_date + dt, end_date)
        continue

    return data_urls


def _get_dates(date_range):
    """Derive start_date and end_date from date_range"""
    start_date, end_date = date_range
    if start_date is None and end_date is None:
        raise ValueError('Either start_date or end_date must be provided.')
    if end_date is None:
        end_date = start_date + datetime.timedelta(days=1)
    elif start_date is None:
        start_date = end_date - datetime.timedelta(days=1)
    t0 = datetime.time()
    if start_date.time() == t0:
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_date.replace(hour=23, minute=59, second=59)
    return start_date, end_date
