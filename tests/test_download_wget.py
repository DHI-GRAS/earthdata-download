import unittest
import os
import logging

from earthdata_download.download_wget import download_data
from earthdata_download import query

from test_params import query_kw, auth

logging.basicConfig(level=logging.DEBUG)

class DownloadTests(unittest.TestCase):

    def test_download_wget(self):

        url = query.url_from_query(**query_kw)
        data_urls = query.get_data_urls(url)
        try:
            local_filename = download_data(data_urls[0], username=auth[0], password=auth[1])
            self.assertTrue(os.path.isfile(local_filename))
        finally:
            # clean up
            try:
                os.remove(local_filename)
            except (WindowsError, OSError):
                pass
