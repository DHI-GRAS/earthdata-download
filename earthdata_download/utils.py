from collections import defaultdict

from earthdata_download import parse


def group_entries_by_date(entries):
    if 'start_date' not in entries[0]:
        entries = [parse.parse_entry(e) for e in entries]

    grouped = defaultdict(list)
    for e in entries:
        date = e['start_date'].date()
        grouped[date].append(e)

    grouped_sorted = {}
    for date in sorted(grouped):
        grouped_sorted[date] = grouped[date]

    return grouped_sorted
