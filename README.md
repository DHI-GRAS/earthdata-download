# earthdata-download
Query and download https://earthdata.nasa.gov/

[![Build Status](https://travis-ci.org/DHI-GRAS/earthdata-download.svg?branch=master)](https://travis-ci.org/DHI-GRAS/earthdata-download)
[![codecov](https://codecov.io/gh/DHI-GRAS/earthdata-download/branch/master/graph/badge.svg)](https://codecov.io/gh/DHI-GRAS/earthdata-download)


## NASA EARTHDATA login

In order to download from NASA's EARTHDATA archives, you need to have a user account at
https://urs.earthdata.nasa.gov.

Note: You need to authorize the applications you want to download from.
Some of the applications the authors most often use are

* LP DAAC Data Pool
* NASA GESDISC DATA ARCHIVE
* GHRC DAAC


## Example

### Query

```python
import datetime

from earthdata_download.api import EarthdataAPI

api = EarthdataAPI('<username>', '<password>')

results = api.query(
    short_name='ATL08', 
    version='002', 
    start_date=datetime.datetime(2018, 1, 1), 
    end_date = datetime.datetime(2020, 1, 1), 
    extent={
        'xmin': 33,
        'xmax': 34,
        'ymin': -14,
        'ymax': -13
    }
)
```

### Query results:

```python
[{'producer_granule_id': 'ATL08_20181016131403_02730114_002_01.h5',
  'time_start': '2018-10-16T13:14:34.000Z',
  'orbit': {'ascending_crossing': '55.413850781199955',
   'start_lat': '-27',
   'start_direction': 'A',
   'end_lat': '0',
   'end_direction': 'A'},
  'updated': '2019-10-24T13:03:44.747Z',
  'orbit_calculated_spatial_domains': [{'equator_crossing_date_time': '2018-10-16T11:46:46.152Z',
    'equator_crossing_longitude': '55.413850781199955',
    'orbit_number': '474'}],
  'dataset_id': 'ATLAS/ICESat-2 L3A Land and Vegetation Height V002',
  'data_center': 'NSIDC_ECS',
  'title': 'SC:ATL08.002:165637357',
  'coordinate_system': 'ORBIT',
  'time_end': '2018-10-16T13:21:09.000Z',
  'id': 'G1642816294-NSIDC_ECS',
  'original_format': 'ISO-SMAP',
  'granule_size': '32.5740604401',
  'browse_flag': True,
  'polygons': [['-24.76888242988511 34.20857178296797 -5.691013212184329 32.250371699159686 0.3504762159254447 31.643708062678925 0.36178165902088644 31.967454018741257 -5.67965210174744 32.57570980728119 -24.75643243655077 34.56504726611832 -24.76888242988511 34.20857178296797']],
  'collection_concept_id': 'C1631076784-NSIDC_ECS',
  'online_access_flag': True,
  'links': [{'rel': 'http://esipfed.org/ns/fedsearch/1.1/data#',
    'type': 'application/x-hdfeos',
    'hreflang': 'en-US',
    'href': 'https://n5eil01u.ecs.nsidc.org/DP7/ATLAS/ATL08.002/2018.10.16/ATL08_20181016131403_02730114_002_01.h5'},
   {'rel': 'http://esipfed.org/ns/fedsearch/1.1/browse#',
    'type': 'image/jpeg',
    'hreflang': 'en-US',
    'href': 'https://n5eil01u.ecs.nsidc.org/DP0/BRWS/Browse.001/2019.10.02/ATL08_20181016131403_02730114_002_01_BRW.default.default1.jpg'},
   ...
```

### Download

```python
local_paths = api.download(results[:1], download_dir='.')
```
