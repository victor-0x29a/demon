from datetime import datetime


def now_to_str(date: datetime.now):
    return date.isoformat()


def str_to_date(date_str: str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
