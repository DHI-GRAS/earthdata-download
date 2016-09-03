import unittest

from earthdata_download import EarthdataAPI
from earthdata_download.query import max_n_products

from test_params import api_query_kw, api_query_kw_more_than_max


class TestAPI(unittest.TestCase):

    def test_api_init(self):
        EarthdataAPI()

    def test_find_data(self):
        api = EarthdataAPI()
        data_urls = api.find_data(**api_query_kw)
        print(data_urls)
        self.assertTrue(len(data_urls) > 0)

    def test_find_more_than_max(self):
        api = EarthdataAPI()
        data_urls = api.find_data(**api_query_kw_more_than_max)
        n_urls = len(data_urls)
        print('Number of retrieved urls: {}'.format(n_urls))
        self.assertTrue(n_urls > max_n_products)
