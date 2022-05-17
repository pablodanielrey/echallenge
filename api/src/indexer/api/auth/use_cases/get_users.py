from typing import Union, Any
from ..repository.auth import AuthRepository, AuthSession
from . import UseCase


class GetUsers(UseCase):

    def __init__(self, repo: AuthRepository):
        self.repo = repo

#     def get_users(self, skip: Optional[int] = None, limit: Optional[int] = None) -> list[User]:
    def handle(self, *args, **kw) -> Union[list[Any],Any,None]:
        with self.repo.session() as session:
            users = session.get_users()
        return users
