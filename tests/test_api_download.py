import os

from earthdata_download.api import EarthdataAPI


def test_api_init_with_credentials(earthdata_credentials):
    EarthdataAPI(**earthdata_credentials)


def test_download_single(api_query_kw, earthdata_credentials, tmpdir):
    api = EarthdataAPI(**earthdata_credentials)
    data_urls = api.query(**api_query_kw)
    tempdir = str(tmpdir.mkdir('download'))

    local_filename = api.download_single(data_urls[0], download_dir=tempdir)
    assert os.path.isfile(local_filename)
    assert os.path.getsize(local_filename) > 1e6
