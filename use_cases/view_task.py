from fastapi.exceptions import HTTPException
from pymongo import collection


class ViewTask:
    def __init__(self, host_collection: collection, ip_address: str):
        self.ip_address = ip_address
        self.host_collection = host_collection

    def call(self):
        self.check_if_exist_client()

        return self.task

    @property
    def task(self):
        task = self.client.get("task")

        if task != {}:
            self.remove_current_task()

        return {
            "name": task.get("name", None),
            "args": task.get("args", None)
        }

    def remove_current_task(self):
        self.host_collection.find_one_and_update(
            {"ip_address": self.ip_address},
            {"$set": {"task": {}}}
        )

    def check_if_exist_client(self):
        self.client = self.host_collection.find_one({"ip_address": self.ip_address})
        if not self.client:
            raise HTTPException(404)
