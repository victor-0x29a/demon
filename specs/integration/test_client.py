import pytest
from . import app
from faker import Faker
from faker.providers import internet
from fastapi.testclient import TestClient
from mongomock import MongoClient
from models import Host, Task


client = TestClient(app)

namespace = "/client"

fake = Faker('pt_BR')
fake.add_provider(internet)


@pytest.fixture
def mock_mongodb():
    return MongoClient().db.collection


class TestHealthCheck:
    def test_with_invalid_ip_address(self):
        response = client.get(f"{namespace}/health-check?ip_address=random")

        assert response.status_code == 422

    def test_without_ip_address(self):
        response = client.get(f"{namespace}/health-check")

        assert response.status_code == 422

    def test_success(self, mocker, mock_mongodb):
        ip = fake.ipv4()

        mock_client = mocker.patch("fastapi.Request.app")
        mock_client.database = {
            "host": mock_mongodb
        }

        response = client.get(f"{namespace}/health-check?ip_address={ip}")

        client_generated = mock_mongodb.find_one({"ip_address": ip})

        assert client_generated

        assert response.status_code == 204

    def test_should_update_an_exists_client(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        host_instance = Host(_id=ip)

        old_client = mock_client.insert_one(host_instance.model_dump())

        client.get(f"{namespace}/health-check?ip_address={ip}")

        new_client = mock_client.find_one({
            "ip_address": ip
        })

        assert old_client["health_check_datetime"] != new_client["health_check_datetime"]


task_content = {
    "task_name": "foo",
    "task_args": ["bar"]
}


class TestTask:
    def test_should_not_add_task_when_doesnt_exist_client(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        request = client.post(f"{namespace}/add-task?ip_address={ip}", json=task_content)

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

        request = client.post(f"{namespace}/add-task?ip_address={ip}", json=task_content)

        assert request.status_code == 409

    def test_should_add_a_task(self, mocker, mock_mongodb):
        mock_client = mocker.patch("fastapi.Request.app")

        mock_client.database = {
            "host": mock_mongodb
        }

        ip = fake.ipv4()

        host = Host(_id=ip).model_dump()

        mock_mongodb.insert_one(host)

        request = client.post(f"{namespace}/add-task?ip_address={ip}", json=task_content)

        assert request.status_code == 204

        host = mock_mongodb.find_one({"ip_address": ip})

        assert host.get("task") is not {}
