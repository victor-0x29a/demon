import pytest
from . import app
from fastapi.testclient import TestClient
from mongomock import MongoClient
from utils import generate_token


client = TestClient(app)

namespace = "/auth"
server_namespace = "/server"


@pytest.fixture
def mock_mongodb():
    return MongoClient().db.collection


class TestAuthentication:
    def test_should_generate_a_token_with_valid_body(self):
        response = client.post(f"{namespace}/gen", json={
            "username": "admin",
            "password": "admin"
        })

        assert response.status_code == 204
        assert response.headers["Authorization"]

    def test_should_reject_all_wrong_data(self):
        payload_list = [
            ["admin1", "admin"],
            ["admin", "admin1"],
            ["ADMIN", "admin"],
            ["foo", "bar"],
            ["admin ", "admin"],
            [" admin ", " admin "]
        ]

        for payload in payload_list:
            response = client.post(f"{namespace}/gen", json={
                "username": payload[0],
                "password": payload[1]
            })

            assert response.status_code == 406


class TestRequiresLoginDecorator:
    def test_should_reject_an_unknown_token(self):
        unknown_token = "unknown"

        response = client.post(
            f"{server_namespace}/task/add",
            headers={
                "Authorization": unknown_token
            })

        assert response.status_code == 401

    def test_should_approve_a_valid_token(self):
        valid_token = generate_token()

        response = client.post(
            f"{server_namespace}/task/add",
            headers={
                "Authorization": valid_token
            })

        assert response.status_code != 401
