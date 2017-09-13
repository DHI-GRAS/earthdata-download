from earthdata_download import EarthdataAPI
from earthdata_download.query import MAX_N_PRODUCTS

from .test_params import api_query_kw, api_query_kw_more_than_max


def test_api_init():
    EarthdataAPI()


def test_find_data():
    api = EarthdataAPI()
    data_urls = api.find_data(**api_query_kw)
    assert len(data_urls) > 0


def test_find_more_than_max():
    api = EarthdataAPI()
    data_urls = api.find_data(**api_query_kw_more_than_max)
    n_urls = len(data_urls)
    assert n_urls > MAX_N_PRODUCTS
