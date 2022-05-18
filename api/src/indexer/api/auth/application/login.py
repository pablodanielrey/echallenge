from typing import Optional, Union, Any

from indexer.api.auth.domain.exceptions import UserNotFound

from ..domain import models, AuthRepository

from . import UseCase


class Login(UseCase):

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    # def handle(self, username: str, password: str) -> Union[list[Any],Any,None]:
    def handle(self, username: str, password: str) -> models.UserWithCredentials:
        user = self.repo.find_by_username(username)
        user.verify_password(password)
        return user
