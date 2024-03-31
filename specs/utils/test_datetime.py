from datetime import datetime
from utils import now_to_str, str_to_date


def test_should_transform_now_to_str():
    now = datetime.now()

    now_str = now_to_str(now)

    assert "str" in str(type(now_str))


def test_should_transform_now_str_to_date():
    now = datetime.now()

    now_str = now_to_str(now)

    assert now == str_to_date(now_str)
