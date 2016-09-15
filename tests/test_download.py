import unittest
import os
import logging

from earthdata_download import download_data, query

from test_params import query_kw, auth

logging.basicConfig(level=logging.DEBUG)

class DownloadTest(unittest.TestCase):

    def test_download(self):

        url = query.url_from_query(**query_kw)
        data_urls = query.get_data_urls(url)
        local_filename = download_data(data_urls[0], username=auth[0], password=auth[1])
        try:
            self.assertTrue(os.path.isfile(local_filename))
        finally:
            # clean up
            try:
                os.remove(local_filename)
            except (WindowsError, OSError):
                pass
