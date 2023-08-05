import datetime


def get_days_from_timedelta(delta: datetime.timedelta):
    return delta.days


def set_negative_to_zero(a: float):
    if a < 0:
        return 0
    else:
        return a


def datetime_to_date(dt: datetime.datetime) -> datetime.date:
    return dt.date()
