from datetime import datetime
from utils import now_to_str, str_to_date, date_in_range


def test_should_transform_now_to_str():
    now = datetime.now()

    now_str = now_to_str(now)

    assert "str" in str(type(now_str))


def test_should_transform_now_str_to_date():
    now = datetime.now()

    now_str = now_to_str(now)

    assert now == str_to_date(now_str)


def test_should_in_range():
    now = datetime.now()

    simulated_date = datetime(now.year, now.month, now.day, now.hour, now.minute - 1)

    max_minute_in_range = 2

    assert date_in_range(simulated_date, max_minute_in_range)


def test_should_not_in_range():
    now = datetime.now()

    simulated_date = datetime(now.year, now.month, now.day, now.hour, now.minute - 1)

    max_minute_in_range = 1

    assert not date_in_range(simulated_date, max_minute_in_range)
