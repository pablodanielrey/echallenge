import pytest
from fastapi.testclient import TestClient

from indexer.api.app import app
from indexer.api.jwt import services, settings


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def jwt_manager():
    jsettings = settings.JWTSettings()
    return services.JWTManager(jsettings.jwt_key,
                             jsettings.jwt_algo,
                             jsettings.jwt_audience,
                             jsettings.jwt_issuer,
                             jsettings.jwt_expire)


@pytest.fixture(scope="session")
def auth_headers(jwt_manager):
    payload = {
        "sub": "username:someuser"
    }
    jwt = jwt_manager.encode_jwt(payload)
    headers = {
        "authorization": f"bearer {jwt}"
    }
    return headers


def test_unsecured_user_creation(client: TestClient):
    response = client.post("/users")
    assert response.status_code == 401


def test_empty_user_creation(client: TestClient, auth_headers):
    response = client.post("/users", headers=auth_headers)
    assert response.status_code == 422


def test_wrong_format_user_creation(client: TestClient, auth_headers):
    response = client.post("/users", json={"name": "Pablo"}, headers=auth_headers)
    assert response.status_code == 422

