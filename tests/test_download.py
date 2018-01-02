import os
import logging

from earthdata_download import download_data
from earthdata_download import query
from earthdata_download import parse

logging.basicConfig(level=logging.DEBUG)


def test_download(query_kw, earthdata_credentials, tmpdir):
    entries = query.find_data_entries(**query_kw)
    data_urls = parse.get_data_urls_from_entries(entries, linkno=0)
    tempdir = str(tmpdir.mkdir('download'))

    local_filename = download_data(
        data_urls[0],
        download_dir=tempdir,
        **earthdata_credentials)
    assert os.path.isfile(local_filename)
