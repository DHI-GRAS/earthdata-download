import datetime

from earthdata_download import parse
from earthdata_download import query

from .test_params import query_kw


def test_parse():
    entries = query.find_data_entries(**query_kw)
    ee = [parse.parse_entry(e) for e in entries]
    e = ee[0]
    assert 'footprint' in e
    assert isinstance(e['start_date'], datetime.datetime)
