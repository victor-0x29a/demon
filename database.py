from pymongo import MongoClient

from constants import MONGO_DB, MONGO_URL


def get_mongo_connection():
    return MongoClient(MONGO_URL)[MONGO_DB]
