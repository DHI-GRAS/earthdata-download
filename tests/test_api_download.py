import tempfile
import shutil
import os.path
import warnings

import pytest

from earthdata_download import EarthdataAPI

from test_params import api_query_kw, auth


def test_api_init():
    EarthdataAPI(**auth)


def test_find_data():
    api = EarthdataAPI(**auth)
    data_urls = api.find_data(**api_query_kw)
    print(data_urls)
    assert (len(data_urls) > 0)


@pytest.mark.skipif(
        (auth['username'] is None or auth['password'] is None),
        reason='invalid or missing authentication')
def test_download_single():
    api = EarthdataAPI(**auth)
    data_urls = api.find_data(**api_query_kw)
    tempdir = tempfile.mkdtemp()
    try:
        local_filename = api.download_single(data_urls[0], download_dir=tempdir)
        assert (os.path.isfile(local_filename))
    finally:
        try:
            shutil.rmtree(tempdir)
        except OSError:
            warnings.warn('Unable to remove tempdir \'%s\'.', tempdir)
            pass
