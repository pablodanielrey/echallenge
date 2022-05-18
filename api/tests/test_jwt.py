import pytest
import time

from indexer.api.jwt import services, settings, exceptions


@pytest.fixture(scope="session")
def jwt_manager():
    jsettings = settings.JWTSettings()
    return services.JWTManager(jsettings.jwt_key,
                             jsettings.jwt_algo,
                             jsettings.jwt_audience,
                             jsettings.jwt_issuer,
                             jsettings.jwt_expire)


@pytest.fixture(scope="session")
def another_jwt_manager():
    jsettings = settings.JWTSettings()
    return services.JWTManager(jsettings.jwt_key,
                             jsettings.jwt_algo,
                             jsettings.jwt_audience,
                             f"{jsettings.jwt_issuer}2",
                             jsettings.jwt_expire)


@pytest.fixture(scope="session")
def expired_jwt_manager():
    jsettings = settings.JWTSettings()
    return services.JWTManager(jsettings.jwt_key,
                             jsettings.jwt_algo,
                             jsettings.jwt_audience,
                             jsettings.jwt_issuer,
                             0)          


def test_generate_jwt(jwt_manager):
    payload = {
        "sub": "somesubject",
        "test": "value1",
        "test2": "value2"
    }
    jwt = jwt_manager.encode_jwt(payload)
    payload2 = jwt_manager.decode_jwt(jwt)
    assert payload == payload2


def test_encode_invalid_jwt(jwt_manager):
    with pytest.raises(exceptions.JWTInvalidFormat):
        payload = {
            "test": "value1",
            "test2": "value2"
        }
        jwt_manager.encode_jwt(payload)


def test_decode_invalid_jwt(jwt_manager):
    payload = {
        "sub": "somesubject"
    }
    jwt = jwt_manager.encode_jwt(payload)
    truncated_jwt = jwt[:-2]

    with pytest.raises(exceptions.JWTException):
        jwt_manager.decode_jwt(truncated_jwt)


def test_decode_invalid2_jwt(jwt_manager, another_jwt_manager):
    payload = {
        "sub": "somesubject"
    }
    jwt = another_jwt_manager.encode_jwt(payload)

    with pytest.raises(exceptions.JWTException):
        jwt_manager.decode_jwt(jwt)


def test_expired_jwt(jwt_manager, expired_jwt_manager):
    payload = {
        "sub": "somesubject"
    }
    jwt = expired_jwt_manager.encode_jwt(payload)
    time.sleep(1)
    with pytest.raises(exceptions.JWTException):
        jwt_manager.decode_jwt(jwt)
