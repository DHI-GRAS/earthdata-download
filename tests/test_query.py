import requests
import json

import pytest

from earthdata_download import query

from .shared import my_vcr


@my_vcr.use_cassette
@pytest.mark.nasa
def test_format_query_url(query_kw):
    """Test generating a url and parsing the output"""
    url = query.format_query_url(**query_kw)
    r = requests.get(url)
    json.loads(r.text)


@my_vcr.use_cassette
@pytest.mark.nasa
def test_get_entries_noparse(query_kw):
    entries = query.get_entries(parse_entries=False, **query_kw)
    assert len(entries) > 0
    assert 'time_start' in entries[0]


@my_vcr.use_cassette
@pytest.mark.nasa
def test_get_entries_parse(query_kw):
    entries = query.get_entries(parse_entries=True, **query_kw)
    assert len(entries) > 0
    assert 'start_date' in entries[0]


@my_vcr.use_cassette
@pytest.mark.nasa
def test_get_entries_more_than_max(api_query_kw_more_than_max):
    entries = query.get_entries(**api_query_kw_more_than_max)
    assert len(entries) > query.MAX_N_PRODUCTS
