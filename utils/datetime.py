from datetime import datetime, timedelta


def now_to_str(date: datetime.now):
    return date.isoformat()


def str_to_date(date_str: str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')


def date_in_range(date: datetime, max_minute: int):
    now = datetime.now()

    interval = timedelta(minutes=max_minute)

    time_limit = now - interval

    return time_limit <= date <= now
