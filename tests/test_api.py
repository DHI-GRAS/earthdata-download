import unittest
import tempfile
import shutil
import os.path

from earthdata_download import EarthdataAPI

from test_params import api_query_kw, auth


class TestAPI(unittest.TestCase):

    def test_api_init(self):
        EarthdataAPI(username=auth[0], password=auth[1])

    def test_find_data(self):
        api = EarthdataAPI(username=auth[0], password=auth[1])
        data_urls = api.find_data(**api_query_kw)
        print(data_urls)
        self.assertTrue(len(data_urls) > 0)

    def test_download_single(self):
        api = EarthdataAPI(username=auth[0], password=auth[1])
        data_urls = api.find_data(**api_query_kw)
        tempdir = tempfile.mkdtemp()
        try:
            local_filename = api.download_single(data_urls[0], download_dir=tempdir)
            self.assertTrue(os.path.isfile(local_filename))
        finally:
            shutil.rmtree(tempdir)

