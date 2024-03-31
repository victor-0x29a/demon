import pytest
from . import app
from faker import Faker
from faker.providers import internet
from fastapi.testclient import TestClient
from mongomock import MongoClient
from models import Host, Task


client = TestClient(app)

namespace = "/server"

fake = Faker('pt_BR')
fake.add_provider(internet)


@pytest.fixture
def mock_mongodb():
    return MongoClient().db.collection


task_content = {
    "task_name": "foo",
    "task_args": ["bar"]
}


class TestAddTask:
    def test_should_not_add_task_when_doesnt_exist_client(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        request = client.post(f"{namespace}/task/add?ip_address={ip}", json=task_content)

        assert request.status_code == 422

    def test_should_not_add_task_when_the_client_already_have_a_task(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        task = Task(name=task_content["task_name"], args=task_content["task_args"]).model_dump()

        host = Host(_id=ip, task=task).model_dump()

        mock_mongodb.insert_one(host)

        request = client.post(f"{namespace}/task/add?ip_address={ip}", json=task_content)

        assert request.status_code == 409

    def test_should_add_a_task(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        host = Host(_id=ip).model_dump()

        mock_mongodb.insert_one(host)

        request = client.post(f"{namespace}/task/add?ip_address={ip}", json=task_content)

        assert request.status_code == 204

        host = mock_mongodb.find_one({"ip_address": ip})

        assert host.get("task") is not {}


class TestRemoveTask:
    def test_should_not_remove_from_an_unexist_client(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        request = client.post(f"{namespace}/task/remove?ip_address={ip}", json=task_content)

        assert request.status_code == 404

    def test_should_remove(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        task = Task(name="foo", args=["bar"]).model_dump()

        host = Host(_id=ip, task=task).model_dump()

        mock_mongodb.insert_one(host)

        host = mock_mongodb.find_one({"ip_address": ip})

        assert host["task"] != {}

        request = client.post(f"{namespace}/task/remove?ip_address={ip}", json=task_content)

        assert request.status_code == 204

        host = mock_mongodb.find_one({"ip_address": ip})

        assert host["task"] == {}

    def test_should_not_request_the_mongo_when_havent_task(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        host = Host(_id=ip).model_dump()

        mock_mongodb.insert_one(host)

        host = mock_mongodb.find_one({"ip_address": ip})

        assert host["task"] == {}

        request = client.post(f"{namespace}/task/remove?ip_address={ip}", json=task_content)

        assert request.status_code == 204

        host = mock_mongodb.find_one({"ip_address": ip})

        assert host["task"] == {}
