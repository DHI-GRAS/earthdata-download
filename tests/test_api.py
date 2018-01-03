import pytest

from earthdata_download.api import EarthdataAPI

from .shared import my_vcr


@pytest.mark.fast
def test_api_init_blank():
    EarthdataAPI()


@my_vcr.use_cassette
@pytest.mark.nasa
def test_query(api_query_kw):
    api = EarthdataAPI()
    entries = api.query(**api_query_kw)
    assert len(entries) > 0
