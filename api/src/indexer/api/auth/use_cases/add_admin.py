from typing import Optional, Union, Any
# from passlib.hash import pbkdf2_sha256

# from sqlalchemy import select, exc
# from sqlalchemy.orm import selectinload

# from pydantic import BaseModel
# from ..repository import entities

from indexer.api.auth.repository import AuthRepository, AuthSession


# from ..repository.exceptions import IntegrityError, IncorrectCredentials, UserNotFound
from .. import schemas
from . import UseCase, models
from . import UseCase


class AddAdmin(UseCase):

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def handle(self, **kw) -> Union[list[Any], Any, None]:
        """
        Genera un admin dentro del sistema.
        No recibe parámetros debido a que ya son conocidos y fijos.
        """
        user = models.UserWithCredentials(
            name="admin",
            lastname="admin",
            email="something@domain.com",
            credentials=[
                models.Credentials(
                    username="admin",
                    password="admin"
                )
            ]
        )
        assert user.credentials is not None
        assert len(user.credentials) == 1

        with self.repo.session() as session:
            uid = session.add_user(user)
            session.commit()

        user.id = uid
        return user