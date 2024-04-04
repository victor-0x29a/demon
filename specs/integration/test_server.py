import pytest
from . import app
from faker import Faker
from utils import now_to_str, generate_token
from models import Host, Task
from datetime import datetime
from mongomock import MongoClient
from faker.providers import internet
from fastapi.testclient import TestClient


client = TestClient(app)

namespace = "/server"
client_namespace = "/client"

fake = Faker('pt_BR')
fake.add_provider(internet)


@pytest.fixture
def mock_mongodb():
    return MongoClient().db.collection


task_content = {
    "task_name": "foo",
    "task_args": ["bar"]
}

default_headers = {
    "Authorization": generate_token()
}


class TestAddTask:
    def test_should_not_add_task_when_doesnt_exist_client(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        request = client.post(
            f"{namespace}/task/add?ip_address={ip}",
            json=task_content,
            headers=default_headers
        )

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

        request = client.post(
            f"{namespace}/task/add?ip_address={ip}",
            json=task_content,
            headers=default_headers
        )

        assert request.status_code == 409

    def test_should_add_a_task(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        host = Host(_id=ip).model_dump()

        mock_mongodb.insert_one(host)

        request = client.post(
            f"{namespace}/task/add?ip_address={ip}",
            json=task_content,
            headers=default_headers
        )

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

        request = client.post(
            f"{namespace}/task/remove?ip_address={ip}",
            json=task_content,
            headers=default_headers
        )

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

        request = client.post(
            f"{namespace}/task/remove?ip_address={ip}",
            json=task_content,
            headers=default_headers
        )

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

        request = client.post(
            f"{namespace}/task/remove?ip_address={ip}",
            json=task_content,
            headers=default_headers
        )

        assert request.status_code == 204

        host = mock_mongodb.find_one({"ip_address": ip})

        assert host["task"] == {}


class TestShowClientsOnline:
    def test_should_show_empty_list(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        request = client.get(f"{namespace}/client/online", headers=default_headers)

        assert request.status_code == 200
        assert request.json() == []

    def test_should_show_an_online_client(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        client.get(f"{client_namespace}/health-check?ip_address={ip}", headers=default_headers)

        request = client.get(f"{namespace}/client/online", headers=default_headers)

        body = request.json()

        assert request.status_code == 200
        assert len(body) == 1

    def test_should_not_show_an_expired_health_check_datetime(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        now = datetime.now()

        """ +1 minute before the time setted in .env.test """
        expired_minute = now.minute - 6

        if expired_minute < 0:
            expired_minute = expired_minute * -1
        elif expired_minute > 59:
            expired_minute = 6

        expired_datetime = datetime(
            now.year,
            now.month,
            now.day,
            now.hour,
            expired_minute
        )

        host = Host(
            _id=ip,
            health_check_datetime=now_to_str(expired_datetime)
        ).model_dump()

        mock_mongodb.insert_one(host)

        request = client.get(f"{namespace}/client/online", headers=default_headers)

        body = request.json()

        assert request.status_code == 200

        assert len(body) == 0
