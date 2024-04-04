import pytz
from datetime import datetime, timedelta
from constants import TIMEZONE


timezone = pytz.timezone(TIMEZONE)


def now_to_str(date: datetime.now):
    parsed_date = timezone.localize(date)
    return datetime.strftime(parsed_date, '%Y-%m-%dT%H:%M:%S.%f')


def str_to_date(date_str: str):
    return timezone.localize(datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f'))


def date_in_range(date: datetime, max_minute: int):
    now = datetime.now()

    now = timezone.localize(now)

    if max_minute > 59:
        max_minute = 1
    elif max_minute < 0:
        max_minute = 59

    interval = timedelta(minutes=max_minute)

    time_limit = now - interval

    return time_limit <= date <= now
