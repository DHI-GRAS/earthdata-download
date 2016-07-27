from __future__ import print_function
import unittest
import requests
import json

from earthdata_download import query
from test_params import query_kw

class DownloadTests(unittest.TestCase):

    def test_url_from_query(self):
        """Test generating a url and parsing the output"""
        url = query.url_from_query(**query_kw)
        print(url)
        r = requests.get(url)
        json.loads(r.text)

    def test_get_data_urls(self):
        url = query.url_from_query(**query_kw)
        data_urls = query.get_data_urls(url)
        print(data_urls)
        self.assertTrue(data_urls[0].endswith('.hdf'))
