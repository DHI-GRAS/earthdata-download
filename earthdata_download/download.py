import os
import posixpath
import logging

from wget_provider import download_url

logger = logging.getLogger('earthdata_download.download')


def download_data(url, username, password, download_dir='.', local_filename=''):
    """Download a url with login using wget"""

    # generate local file name
    if not local_filename:
        local_filename = os.path.join(download_dir, posixpath.basename(url))

    download_url(url,
            auth=dict(username=username, password=password),
            continue_partial=True,
            local_filename=local_filename)

    return local_filename
