from dotenv import dotenv_values


config = dotenv_values(".env")


MONGO_URL = config["MONGO_URL"]
MONGO_DB = config["MONGO_DB"]

IPV4_REGEX = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
