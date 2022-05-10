import uuid
import pytest

from api.auth import exceptions, entities, deps


@pytest.fixture(scope="session")
def user_manager():
    um = deps.get_users_manager()
    um.db.drop_db()
    um.db.generate_db()
    yield um
    um.db.drop_db()


@pytest.fixture(scope="session")
def users():
    return [{"name": f"u{n}", "lastname": f"l{n}", "email": f"m{n}@gmail", "username": f"u{n}", "password": f"p{n}"} for n in range(10)]


def test_add_users(user_manager, users):
    for u in users:
        uid = user_manager.add_user(**u)
        assert uid is not None
        assert type(uid) is uuid.UUID
        assert uuid.UUID(str(uid), version=4)


def test_add_dup_user(user_manager, users):
    for u in users:
        with pytest.raises(exceptions.IntegrityError):
            user_manager.add_user(**u)


def test_add_dup_credentials(user_manager, users):
    for u in users:
        with pytest.raises(exceptions.IntegrityError):
            user_manager.add_user(name="alguien", lastname="queno", email="existe@gmail.com", username=u["username"], password="clavenueva")


def test_incorrect_login(user_manager):
    with pytest.raises(exceptions.AuthError):
        user_manager.login(username="algo", password="incorrecto")


def test_login(user_manager, users):
    for u in users:
        user = user_manager.login(username=u["username"], password=u["password"])
        assert user
        assert type(user) is entities.User
        assert user.email == u["email"]


def _filter_keys(d: dict, keys: list[str] = ["name", "lastname", "email"]):
    return {k: v for k, v in d.items() if k in keys}


def test_get_users(user_manager, users):
    rusers = user_manager.get_users()
    assert rusers
    assert len(rusers) == len(users)
    for k, u in enumerate(rusers):
        assert u.email == users[k]["email"]
        assert _filter_keys(u.__dict__) == _filter_keys(users[k])
