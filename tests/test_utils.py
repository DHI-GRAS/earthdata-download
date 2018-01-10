import datetime

import pytest

from earthdata_download import utils
from earthdata_download import query

from .shared import my_vcr


@my_vcr.use_cassette
@pytest.mark.nasa
def test_group_entries_by_date(query_kw):
    entries = query.get_entries(parse_entries=False, **query_kw)
    grouped = utils.group_entries_by_date(entries)
    firstkey = next(iter(grouped.keys()))
    assert isinstance(firstkey, datetime.date)
    firstitem = next(iter(grouped.values()))
    assert isinstance(firstitem, list)
    assert len(firstitem) > 0
    assert isinstance(firstitem[0], dict)


@my_vcr.use_cassette
@pytest.mark.nasa
def test_group_entries_by_date_parsed(query_kw):
    entries = query.get_entries(parse_entries=True, **query_kw)
    grouped = utils.group_entries_by_date(entries)
    firstkey = next(iter(grouped.keys()))
    assert isinstance(firstkey, datetime.date)
    firstitem = next(iter(grouped.values()))
    assert isinstance(firstitem, list)
    assert len(firstitem) > 0
    assert isinstance(firstitem[0], dict)
