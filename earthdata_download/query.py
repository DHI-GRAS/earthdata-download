import json
import requests

nasa_echo_url_base = 'https://api.echo.nasa.gov/catalog-rest/echo_catalog/granules.json?page_num=1'

def url_from_query(short_name='', version='', date_range=(), extent={}):

    url = nasa_echo_url_base

    # currently the API only allows for 2000 files at a time
    url += '&page_size=2000'

    if short_name:
        url += '&short_name={}'.format(short_name)

    if version:
        url += '&version={}'.format(version)

    if date_range:
        url += '&temporal[]={},{}'.format(*[d.strftime('%Y-%m-%dT23:59:59') for d in date_range])

    if extent:
        url += '&bounding_box={xmin},{ymin},{xmax},{ymax}'.format(**extent)

    return url


def get_data_urls(url):

    r = requests.get(url)

    catalogue = json.loads(r.text)
    try:
        entries = catalogue['feed']['entry']
    except KeyError:
        raise ValueError('Query with url \'{}\' did not return any files. '
                'Catalogue:\n\n{}'.format(url, catalogue.__repr__()))

    data_urls = [e['links'][0]['href'] for e in entries]

    return data_urls

