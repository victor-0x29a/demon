from fastapi.exceptions import HTTPException, ValidationException
from pymongo.collection import Collection
from models import Task


class AddTask:
    def __init__(
        self,
        ip_address: str,
        task_name: str,
        task_args: list[str],
        host_collection: Collection
    ):
        self.task_name = task_name
        self.ip_address = ip_address
        self.task_args = task_args
        self.host_collection = host_collection

    def call(self):
        self.validate_data()

        has_client = self.verify_if_client_exist()

        if not has_client:
            raise HTTPException(422, "Verify the client.")

        has_task = self.verify_if_already_have_task()

        if has_task:
            raise HTTPException(409, "Already have a task.")

        self.add_task()

    def validate_data(self):
        if not self.task_name:
            raise ValidationException(["The name is required."])

        is_a_list = "list" in str(type(self.task_args))

        if not is_a_list:
            raise ValidationException(["The args should is a list."])

    def add_task(self):
        task = Task(name=self.task_name, args=self.task_args)
        self.host_collection.find_one_and_update({"ip_address": self.ip_address}, {
            "$set": {"task": task.model_dump()}
        })

    def verify_if_already_have_task(self):
        return not self.client.get("task") == {}

    def verify_if_client_exist(self):
        self.client = self.host_collection.find_one({"ip_address": self.ip_address})
        return self.client is not None
