import os
import datetime

import pytest


@pytest.fixture
def earthdata_credentials():
    varmap = dict(
        username='EARTHDATA_USERNAME',
        password='EARTHDATA_PASSWORD')
    authkw = {k: os.environ.get(v) for k, v in varmap.items()}
    if None in list(authkw.values()):
        raise ValueError(
            'This fixture only works when environment variables {} are defined.'
            .format(list(varmap.values())))
    return authkw


@pytest.fixture
def query_kw():
    return dict(
        short_name='MOD13C1',
        version='005',
        start_date=datetime.datetime(2016, 1, 1),
        end_date=datetime.datetime(2016, 3, 31),
        extent=dict(xmin=30, xmax=40, ymin=-10, ymax=0))


@pytest.fixture
def api_query_kw():
    return dict(
        short_name='MOD13C1',
        version='005',
        start_date=datetime.datetime(2016, 1, 1),
        end_date=datetime.datetime(2016, 3, 31),
        extent=dict(xmin=30, xmax=40, ymin=-10, ymax=0))


@pytest.fixture
def api_query_kw_more_than_max():
    return dict(
        short_name='MOD11A2',
        version='005',
        start_date=datetime.datetime(2016, 1, 1),
        end_date=datetime.datetime(2016, 3, 30))


@pytest.fixture
def sample_extent_small():
    return '-1,1,5,6'


def pytest_addoption(parser):
    parser.addoption(
        "--vcr",
        choices=("use", "disable", "record_new", "reset"),
        default="use",
        help=("Set how prerecorded queries are used:\n"
              "use - replay cassettes but do not record (default),\n"
              "disable - pass all queries directly to the server\n"
              "record_new - replay cassettes and record any unmatched queries,\n"
              "reset - re-record all matching cassettes."))
