from __future__ import print_function
import unittest
import requests
import json

from earthdata_download import downloader
from test_params import query_kw

class DownloadTests(unittest.TestCase):

    def test_url_from_query(self):
        """Test generating a url and parsing the output"""
        url = downloader.url_from_query(**query_kw)
        print(url)
        r = requests.get(url)
        json.loads(r.text)

    def test_get_data_urls(self):

        url = downloader.url_from_query(**query_kw)
        links = downloader.get_data_links(url)
        print(links)
        self.assertTrue(links[0].endswith('.hdf'))
