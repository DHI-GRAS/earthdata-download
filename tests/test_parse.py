import datetime

from earthdata_download import parse
from earthdata_download import query


def test_parse(query_kw):
    entries = query.find_data_entries(**query_kw)
    ee = [parse.parse_entry(e) for e in entries]
    e = ee[0]
    assert 'footprint' in e
    assert isinstance(e['start_date'], datetime.datetime)
