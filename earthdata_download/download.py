import os
import posixpath
import logging
from contextlib import closing

import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)

SERVER_CONTINUING = False


def download_url(
        url, username, password,
        local_filename=None, download_dir=None,
        headers={}, server_supports_continuing=SERVER_CONTINUING):

    auth = requests.auth.HTTPBasicAuth(
            username=username, password=password)

    if local_filename is not None:
        path = local_filename
    else:
        path = os.path.join(download_dir, posixpath.basename(url))

    headers = headers.copy()
    continuing = os.path.exists(path)
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
        with open(path, mode) as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    progress.update(len(chunk))
                    downloaded_bytes += len(chunk)

    return local_filename


def download_data(url, username, password, download_dir='.', local_filename=None, **kwargs):
    """Download a url with login"""

    # generate local file name
    if not local_filename:
        local_filename = os.path.join(download_dir, posixpath.basename(url))

    download_url(
            url,
            username=username,
            password=password,
            local_filename=local_filename, **kwargs)

    return local_filename
