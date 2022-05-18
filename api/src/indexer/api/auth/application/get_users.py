from typing import Optional, Union, Any

from ..domain import models, AuthRepository

from . import UseCase


class GetUsers(UseCase):

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def handle(self, skip: int = 0, limit: int = 0) -> Union[list[Any],Any,None]:
        users = self.repo.find_all(skip, limit)
        return users
