import os
from dotenv import dotenv_values

IS_TEST_ENVIRONMENT = bool(os.environ.get("FASTAPI_ENV") == "test")

config = dotenv_values(".env" if not IS_TEST_ENVIRONMENT else ".env.test")

MONGO_URL = config["MONGO_URL"]
MONGO_DB = config["MONGO_DB"]

IPV4_REGEX = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
CLIENT_HEALTH_CHECK_LOOP_TIME = int(config["CLIENT_HEALTH_CHECK_LOOP_TIME"])

TIMEZONE = config["TIMEZONE"]

SECRET = config["SECRET"]
