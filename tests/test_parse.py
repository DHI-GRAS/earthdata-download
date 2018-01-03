import datetime

import pytest

from earthdata_download import parse
from earthdata_download import query

from .shared import my_vcr


@my_vcr.use_cassette
@pytest.mark.nasa
def test_parse(query_kw):
    entries = query.get_entries(parse_entries=False, **query_kw)
    ee = [parse.parse_entry(e) for e in entries]
    e = ee[0]
    assert 'footprint' in e
    assert isinstance(e['start_date'], datetime.datetime)
