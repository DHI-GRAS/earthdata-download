import os
import logging

from earthdata_download import query
from earthdata_download import download

logging.basicConfig(level=logging.DEBUG)


def test_download(query_kw, earthdata_credentials, tmpdir):
    tempdir = str(tmpdir.mkdir('download'))
    entries = query.get_entries(**query_kw)
    local_filename = download.download_entry(
        entries[0],
        download_dir=tempdir,
        **earthdata_credentials)
    assert os.path.isfile(local_filename)
    assert os.path.getsize(local_filename) > 1e6
