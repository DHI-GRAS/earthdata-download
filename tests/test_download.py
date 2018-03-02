import os

import pytest

from .shared import my_vcr


@pytest.mark.nasa
def test_download(query_kw, earthdata_credentials, tmpdir):
    from earthdata_download import query
    from earthdata_download import download
    tempdir = str(tmpdir)
    entries = query.get_entries(**query_kw)
    local_filename = download.download_entry(
        entries[0],
        download_dir=tempdir,
        **earthdata_credentials)
    assert os.path.isfile(local_filename)
    assert os.path.abspath(os.path.dirname(local_filename)) == os.path.abspath(tempdir)
    assert os.path.getsize(local_filename) > 1e6


@my_vcr.use_cassette
@pytest.mark.nasa
def test_download_gesdisc_unauthorized(query_kw, earthdata_credentials, tmpdir):
    from earthdata_download import download
    gesdisc_url = (
        'http://disc2.gesdisc.eosdis.nasa.gov/data/'
        'TRMM_RT/TRMM_3B42RT_Daily.7/2016/12/3B42RT_Daily.20161231.7.nc4')
    with pytest.raises(RuntimeError):
        download.download_url(gesdisc_url, download_dir=str(tmpdir), **earthdata_credentials)
