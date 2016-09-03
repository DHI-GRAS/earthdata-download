import datetime

start_date, end_date = datetime.datetime(2016,1,1), datetime.datetime(2016,3,31)

query_kw = dict(
        short_name='MOD13C1',
        version='005',
        date_range=(start_date, end_date),
        extent=dict(xmin=30, xmax=40, ymin=-10, ymax=0)
       )

api_query_kw = dict(
        short_name='MOD13C1',
        version='005',
        start_date=start_date,
        end_date=end_date,
        extent=dict(xmin=30, xmax=40, ymin=-10, ymax=0))

auth = ('Jessen5678', 'Drought2016')
