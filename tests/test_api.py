import pytest

from earthdata_download.api import EarthdataAPI
from earthdata_download.query import MAX_N_PRODUCTS


@pytest.mark.fast
def test_api_init_blank():
    EarthdataAPI()


@pytest.mark.nasa
def test_query(api_query_kw):
    api = EarthdataAPI()
    entries = api.query(**api_query_kw)
    assert len(entries) > 0


@pytest.mark.nasa
def test_query_more_than_max(api_query_kw_more_than_max):
    api = EarthdataAPI()
    entries = api.query(**api_query_kw_more_than_max)
    assert len(entries) > MAX_N_PRODUCTS
