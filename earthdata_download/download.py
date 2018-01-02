import os
import shutil
import logging
import posixpath

try:
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    from urlparse import urlparse

import ftputil
import ftputil.error
import requests

from earthdata_download import parse

logger = logging.getLogger(__name__)

EXTENSIONS = ['.hdf', '.zip', '.nc4', '.nc']
SCHEMES = ['https', 'http', 'ftp']


def find_data_url(urls, extensions=EXTENSIONS, no_opendap=True):
    """Find URL that starts with https and ends with a data file extension"""
    urls_schemes = {}
    for url in urls:
        if no_opendap and 'opendap' in url:
            continue
        o = urlparse(url)
        if o.scheme in SCHEMES:
            if posixpath.splitext(o.path)[1] in EXTENSIONS:
                urls_schemes[o.scheme] = url
    for scheme in SCHEMES:
        # prefer https
        if scheme in urls_schemes:
            return urls_schemes[scheme]
    raise ValueError('No HTTPS or FTP data URL found among URLs {}'.format(urls))


def data_url_from_entry(entry):
    """Get data URL from entry"""
    all_urls = parse.get_entry_urls(entry)
    return find_data_url(all_urls)


def _download_file_https(url, target, username, password):
    target_temp = target + '.incomplete'
    with requests.Session() as session:
        session.auth = (username, password)
        login_response = session.get(url)
        with session.get(login_response.url, stream=True) as response:
            response.raise_for_status()
            response.raw.decompress_content = True
            with open(target_temp, "wb") as target_file:
                shutil.copyfileobj(response.raw, target_file)
    shutil.move(target_temp, target)


def _hostname_path_from_url(url):
    o = urlparse(url)
    return o.netloc, o.path


def _download_file_ftp(url, target, username, password):
    hostname, path = _hostname_path_from_url(url)
    try:
        with ftputil.FTPHost(hostname, username, password) as host:
            host.download(path, target)
    except ftputil.error.PermanentError:
        raise ValueError(
                'Unable to connect to this ftp server \'{}\'. '
                'Consider downloading manually \'{}\'.'
                .format(hostname, url))


def download_url(
        url, username, password, download_dir='.',
        local_filename=None, skip_existing=False):
    """Download file from URL with login

    Parameters
    ----------
    url : str
        URL to download
    username, password : str
        credentials
    download_dir : str, optional
        path to download directory
        server-side file name will be used
    local_filename : str, optional
        use instead of download_dir
    skip_existing : bool
        assume existing files are complete
        and skip

    Returns
    -------
    str
        path to downloaded file

    Notes
    -----
    See also https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python
    """
    logger.debug('Downloading %s', url)
    credentials = dict(username=username, password=password)

    o = urlparse(url)
    local_filename = os.path.join(download_dir, posixpath.basename(o.path))

    if os.path.isfile(local_filename) and skip_existing:
        pass
    else:
        if o.scheme == 'ftp':
            _download_file_ftp(url, local_filename, **credentials)
        else:
            _download_file_https(url, local_filename, **credentials)
    return local_filename


def download_entry(entry, **kwargs):
    """Determine data URL from entry and download

    Parameters
    ----------
    entry : dict
        product entry
    **kwargs : additional keyword arguments
        passed to download_url

    Returns
    -------
    str
        path to downloaded file
    """
    url = data_url_from_entry(entry)
    return download_url(url, **kwargs)
