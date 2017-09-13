import datetime
import os

start_date = datetime.datetime(2016, 1, 1)
end_date = datetime.datetime(2016, 3, 31)

query_kw = dict(
        short_name='MOD13C1',
        version='005',
        start_date=start_date,
        end_date=end_date,
        extent=dict(xmin=30, xmax=40, ymin=-10, ymax=0))

api_query_kw = dict(
        short_name='MOD13C1',
        version='005',
        start_date=start_date,
        end_date=end_date,
        extent=dict(xmin=30, xmax=40, ymin=-10, ymax=0))

api_query_kw_more_than_max = dict(
        short_name='MOD11A2',
        version='005',
        start_date=datetime.datetime(2016, 1, 1),
        end_date=datetime.datetime(2016, 3, 30))

auth = dict(
        username=os.environ.get('EARTHDATA_USERNAME'),
        password=os.environ.get('EARTHDATA_PASSWORD'))
