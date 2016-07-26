import datetime

query_kw = dict(
        short_name='MOD13C1',
        version='005',
        date_range=(datetime.datetime(2016,1,1), datetime.datetime(2016,3,31)),
        extent=dict(xmin=30, xmax=40, ymin=-10, ymax=0)
       )

auth = ('Jessen5678', 'Drought2016')
#auth = ('josl', 'ejoHDl$5AI!n')
