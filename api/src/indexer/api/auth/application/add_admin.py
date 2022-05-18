from typing import Optional, Union, Any

from ..domain import models, AuthRepository

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

        uid = self.repo.add(user=user)
        ruser = self.repo.find(uid)
        return ruser