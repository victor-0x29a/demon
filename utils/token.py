import pytz
from jose import jwt
from datetime import datetime, timedelta
from constants import TIMEZONE, SECRET

timezone = pytz.timezone(TIMEZONE)

algorithm = "HS256"


def generate_token():
    expire_datetime = timezone.localize(datetime.now()) + timedelta(minutes=10)

    jwt_payload = {
        "exp": expire_datetime
    }

    token = jwt.encode(jwt_payload, SECRET, algorithm=algorithm)

    return token