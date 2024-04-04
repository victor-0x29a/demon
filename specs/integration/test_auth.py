import pytest
from . import app
from fastapi.testclient import TestClient
from mongomock import MongoClient


client = TestClient(app)

namespace = "/auth"


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
