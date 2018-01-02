import os

from earthdata_download import EarthdataAPI


def test_api_init(earthdata_credentials):
    EarthdataAPI(**earthdata_credentials)


def test_find_data(api_query_kw, earthdata_credentials):
    api = EarthdataAPI(**earthdata_credentials)
    data_urls = api.find_data(**api_query_kw)
    print(data_urls)
    assert (len(data_urls) > 0)


def test_download_single(api_query_kw, earthdata_credentials, tmpdir):
    api = EarthdataAPI(**earthdata_credentials)
    data_urls = api.find_data(**api_query_kw)
    tempdir = str(tmpdir.mkdir('download'))

    local_filename = api.download_single(data_urls[0], download_dir=tempdir)
    assert os.path.isfile(local_filename)
    assert os.path.getsize(local_filename) > 1e6
