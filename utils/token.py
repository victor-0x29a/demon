from datetime import datetime, timezone


def generate_token():
    expire_datetime = datetime.now()
