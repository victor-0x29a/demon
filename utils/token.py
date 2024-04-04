import pytz
from jose import jwt
from datetime import datetime, timedelta
from constants import TIMEZONE, SECRET, ALGORITHM

timezone = pytz.timezone(TIMEZONE)

algorithm = ALGORITHM


def generate_token():
    expire_datetime = timezone.localize(datetime.now()) + timedelta(minutes=10)

    jwt_payload = {
        "exp": expire_datetime
    }

    token = jwt.encode(jwt_payload, SECRET, algorithm=algorithm)

    return token


def token_is_valid(token, secret):
    try:
        jwt.decode(token=token, key=SECRET)
        return True
    except Exception:
        return False
