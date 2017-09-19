import copy


def _get_entry_urls(e):
    links = e['links']
    return [link['href'] for link in links]


def _join_polygons(polygons):
    import shapely.geometry
    if len(polygons) == 0:
        return None
    elif len(polygons) == 1:
        return polygons[0]
    else:
        return shapely.geometry.MultiPolygon(polygons)


def _parse_polygons(e):
    import shapely.geometry
    polygons = []
    for pstr in e['polygons'][0]:
        cc = [float(s) for s in pstr.split(' ')]
        # cpairs = list(zip(cc[:-1:2], cc[1::2]))  # source has x,y pairs
        cpairs = list(zip(cc[1::2], cc[:-1:2]))  # source has y,x pairs!
        polygon = shapely.geometry.Polygon(cpairs)
        polygons.append(polygon)
    return _join_polygons(polygons)


def _parse_boxes(e):
    import shapely.geometry
    polygons = []
    for pstr in e['boxes']:
        cc = [float(s) for s in pstr.split(' ')]
        ymin, xmin, ymax, xmax = cc
        polygon = shapely.geometry.box(xmin, ymin, xmax, ymax, ccw=True)
        polygons.append(polygon)
    return _join_polygons(polygons)


def _get_entry_footprint(e):
    if 'polygons' in e:
        return _parse_polygons(e)
    elif 'boxes' in e:
        return _parse_boxes(e)
    else:
        return None


def parse_entry(e):
    """Parse entry from CMR JSON response"""
    d = {}
    d['original_response'] = copy.deepcopy(e)
    d['urls'] = _get_entry_urls(e)
    d['start_date'] = get_entry_start_date(e)
    d['end_date'] = get_entry_end_date(e)
    d['footprint'] = _get_entry_footprint(e)
    return d


def get_data_urls_from_entries(entries, linkno=0):
    """Get data URLs from entries

    Parameters
    ----------
    entries : list of dict
        entries from JSON response
    linkno : int
        number of link to get
    """
    all_href = [e['links'][linkno]['href'] for e in entries]
    return [url for url in all_href if not url.endswith('.jpg')]


def get_entry_start_date(e):
    """Returns start date for entry"""
    import dateutil.parser
    return dateutil.parser.parse(e['time_start'])


def get_entry_end_date(e):
    """Returns end date for entry"""
    import dateutil.parser
    return dateutil.parser.parse(e['time_end'])
