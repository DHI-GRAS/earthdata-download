import requests
import json

from earthdata_download import query
from .test_params import query_kw


def test_url_from_query():
    """Test generating a url and parsing the output"""
    url = query.url_from_query(**query_kw)
    r = requests.get(url)
    json.loads(r.text)


def test_find_data():
    data_urls = query.find_data(**query_kw)
    assert data_urls[0].endswith('.hdf')


def test_find_data_entries():
    entries = query.find_data_entries(parse_entries=False, **query_kw)
    assert len(entries) > 0
    assert 'time_start' in entries[0]


def test_find_data_entries_parse():
    entries = query.find_data_entries(parse_entries=True, **query_kw)
    assert len(entries) > 0
    assert 'start_date' in entries[0]
