import os
import shutil
import warnings
import tempfile
import logging

import pytest

from earthdata_download import download_data
from earthdata_download import query
from earthdata_download import parse

from .test_params import query_kw, auth

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.skipif(
        (auth['username'] is None or auth['password'] is None),
        reason='invalid or missing authentication')
def test_download():
    entries = query.find_data_entries(**query_kw)
    data_urls = parse.get_data_urls_from_entries(entries, linkno=0)
    tempdir = tempfile.mkdtemp()
    try:
        local_filename = download_data(data_urls[0], download_dir=tempdir, **auth)
        try:
            assert os.path.isfile(local_filename)
        finally:
            try:
                os.remove(local_filename)
            except OSError:
                pass
    finally:
        try:
            shutil.rmtree(tempdir)
        except OSError:
            warnings.warn('Unable to remove tempdir \'%s\'.', tempdir)
