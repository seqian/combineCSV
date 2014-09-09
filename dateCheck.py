from datetime import datetime

__author__ = 'Seqian Wang'


def ensure_proper_format(date):
    # Assumes YYYY MM DD, can get rid of separators
    date = ''.join(filter(lambda x: x.isdigit(), str(date)))
    if len(date) != 8:
        return False
    format_date = lambda d: d[:4] + "-" + d[4:6] + "-" + d[6:8]
    date = format_date(date)
    return date


def return_closest_date(dates_list, date):
    date = ensure_proper_format(date)
    dates_list = [ensure_proper_format(x) for x in dates_list]

    get_datetime = lambda y: datetime.strptime(y, "%Y-%m-%d")
    closest_date = min(dates_list, key=lambda d: abs(get_datetime(d) - get_datetime(date)))
    return dates_list.index(closest_date)