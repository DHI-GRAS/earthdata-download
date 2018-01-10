import os

import pytest

from earthdata_download import query
from earthdata_download import download


@pytest.mark.nasa
def test_download(query_kw, earthdata_credentials, tmpdir):
    tempdir = str(tmpdir)
    entries = query.get_entries(**query_kw)
    local_filename = download.download_entry(
        entries[0],
        download_dir=tempdir,
        **earthdata_credentials)
    assert os.path.isfile(local_filename)
    assert os.path.abspath(os.path.dirname(local_filename)) == os.path.abspath(tempdir)
    assert os.path.getsize(local_filename) > 1e6
