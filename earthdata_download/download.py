import os
import shutil
import posixpath
import logging
from contextlib import closing

import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)

SERVER_CONTINUING = False


def _download_url(
        url, username, password,
        local_filename=None, download_dir='.',
        headers={}, skip_existing=False,
        server_supports_continuing=SERVER_CONTINUING):
    """Download a URL in chunks of 1 MB using requests

    Parameters
    ----------
    url : str
        URL to download
    username, password : str
        credentials
    local_filename : str, optional
        use instead of download_dir
    download_dir : str, optional
        directory to download to
        file name will be server-side file name
    headers : dict
        request headers
    skip_existing : bool
        always skip existing files
    server_supports_continuing : bool
        whether the server is expected to
        support continuing partial
        downloads
    """
    auth = requests.auth.HTTPBasicAuth(
            username=username, password=password)

    path = local_filename
    if not path:
        path = os.path.join(download_dir, posixpath.basename(url))
    path_temp = path + '.incomplete'

    headers = headers.copy()
    continuing = os.path.exists(path)

    if continuing and skip_existing:
        return path

    if continuing and server_supports_continuing:
        already_downloaded_bytes = os.path.getsize(path)
        headers.update(
                {'Range': 'bytes={}-'.format(already_downloaded_bytes)})
    else:
        already_downloaded_bytes = 0

    tqdm_kw = dict(
            desc="Downloading",
            unit="B",
            unit_scale=True,
            initial=already_downloaded_bytes)

    with closing(requests.get(url, stream=True, auth=auth, headers=headers)) as r, \
            closing(tqdm(**tqdm_kw)) as progress:
        chunk_size = 2 ** 20  # download in 1 MB chunks
        mode = 'wb'
        downloaded_bytes = 0
        with open(path_temp, mode) as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    progress.update(len(chunk))
                    downloaded_bytes += len(chunk)
    shutil.move(path_temp, path)
    return path


def download_data(
        url, username, password, download_dir='.',
        local_filename=None, skip_existing=False, **kwargs):
    """Download a url with login

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
    kwargs : keyword arguments
        passed to _download_url
    """
    return _download_url(
            url,
            username=username,
            password=password,
            local_filename=local_filename,
            download_dir=download_dir,
            skip_existing=skip_existing,
            **kwargs)
