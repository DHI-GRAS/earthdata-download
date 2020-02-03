import json
import logging
import datetime

import requests

from earthdata_download import parse

logger = logging.getLogger(__name__)

NASA_ECHO_URL_BASE = 'https://cmr.earthdata.nasa.gov/search/granules.json'
MAX_N_PRODUCTS = 2000
MAX_NUM_PAGES = 100

_TZERO = datetime.time()


def _date_logic(start_date, end_date):
    """Get start and end dates

    Defaults
    --------
    end_date : start_date + 1 day
    start_date : end_date - 1 day

    Returns
    -------
    start_date, end_date
    """
    if start_date is None and end_date is None:
        return None, None
    elif end_date is None:
        end_date = start_date + datetime.timedelta(days=1)
    elif start_date is None:
        start_date = end_date - datetime.timedelta(days=1)
    if start_date.time() == _TZERO:
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_date.replace(hour=23, minute=59, second=59)
    return start_date, end_date


def format_query_url(
        short_name=None, version=None,
        start_date=None, end_date=None, extent=None,
        n_products=MAX_N_PRODUCTS, page_num=1):
    """Generate EarthData query url for given parameters

    Parameters
    ----------
    short_name : str, optional
        product short name
    version : str, optional
        product version (e.g. '005', leading zeros matter!)
    start_date, end_date : datetime.datetime, optional
        date range
    extent : dict, optional
        extent dictionary
        must have entries xmin, xmax, ymin, ymax
    n_products : int (max MAX_N_PRODUCTS)
        number of products to retrieve
    page_num : int
        page to get

    Details
    -------
    https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html
    """
    url = NASA_ECHO_URL_BASE + '?'

    url += 'page_num={}'.format(page_num)

    if n_products > MAX_N_PRODUCTS:
        raise ValueError(
                'Currently, the API only allows for {} products at a time'
                ''.format(MAX_N_PRODUCTS))
    url += '&page_size={}'.format(n_products)

    if short_name:
        url += '&short_name={}'.format(short_name)

    if version:
        url += '&version={}'.format(version)

    start_date, end_date = _date_logic(start_date, end_date)
    if start_date is not None and end_date is not None:
        datefmt = '%Y-%m-%dT%H:%M:%S'
        url += '&temporal[]={},{}'.format(*[d.strftime(datefmt) for d in (start_date, end_date)])

    if extent:
        url += '&bounding_box={xmin},{ymin},{xmax},{ymax}'.format(**extent)

    return url


def _get_entries_from_url(url):
    """Get entries from query url

    Parameters
    ----------
    url : str
        REST query url
    """
    r = requests.get(url)
    try:
        catalogue = json.loads(r.text)
    except ValueError:
        raise RuntimeError('API call did not return JSON: {}'.format(r.text))
    try:
        return catalogue['feed']['entry']
    except KeyError:
        return []


def get_entries(
        short_name='', version='',
        start_date=None, end_date=None,
        extent={}, parse_entries=False):
    """Query EarthData for products and return entry dictionaries

    Parameters
    ----------
    short_name : str
        product short name
    version : str
        product version (e.g. '005', leading zeros matter!)
    start_date, end_date : datetime.datetime
        date range
        can be None
    extent : dict
        extent dictionary
        must have entries xmin, xmax, ymin, ymax
    parse_entries : bool
        parse_entries entries to Python types
        see parse_entries.parse_entry
    """
    # iterate until the full query period has been retrieved
    entries = []
    for page_num in range(1, MAX_NUM_PAGES + 1):
        url = format_query_url(
                short_name=short_name, version=version,
                start_date=start_date,
                end_date=end_date,
                extent=extent,
                n_products=MAX_N_PRODUCTS,
                page_num=page_num)
        logger.debug('Query URL is \'%s\'.', url)
        new_entries = _get_entries_from_url(url)
        if not new_entries:
            # no entries found
            break
        logger.debug('Number of entries on page %d was %d', page_num, len(new_entries))
        entries += new_entries

        # check if there might be more
        if len(entries) < MAX_N_PRODUCTS:
            # nope
            break

    logger.debug('Query returned a total of %d entries.', len(entries))

    if parse_entries:
        return [parse.parse_entry(e) for e in entries]
    else:
        return entries
