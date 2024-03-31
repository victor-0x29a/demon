from fastapi.exceptions import HTTPException
from pymongo import collection


class RemoveTask:
    def __init__(self, host_collection: collection, ip_address: str):
        self.host_collection = host_collection
        self.ip_address = ip_address

    def call(self):
        self._verify_if_exist_client()

        if self.client["task"] == {}:
            return

        self._remove_task()

    def _remove_task(self):
        self.host_collection.find_one_and_update(
            {"ip_address": self.ip_address},
            {"$set": {"task": {}}}
        )

    def _verify_if_exist_client(self):
        self.client = self.host_collection.find_one({"ip_address": self.ip_address})

        if not self.client:
            raise HTTPException(404)
