import pytest

from .shared import my_vcr


@pytest.mark.fast
def test_api_init_blank():
    from earthdata_download.api import EarthdataAPI
    EarthdataAPI()


@my_vcr.use_cassette
@pytest.mark.nasa
def test_query(api_query_kw):
    from earthdata_download.api import EarthdataAPI
    api = EarthdataAPI()
    entries = api.query(**api_query_kw)
    assert len(entries) > 0
