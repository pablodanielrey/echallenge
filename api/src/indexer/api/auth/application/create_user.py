from typing import Optional, Union, Any

from ..domain import models, AuthRepository

from . import UseCase


class CreateUser(UseCase):

    def __init__(self, repo: AuthRepository):
        self.repo = repo


    def handle(self, name: str, lastname: str, email: str, username: str, password: str) -> Union[list[Any], Any, None]:
        """
        Genera un usuario dentro del sistema.
        Returns:
            id: retorna el id del usuario creado
        """
        user = models.UserWithCredentials(
            name=name,
            lastname=lastname,
            email=email,
            credentials=[
                models.Credentials(
                    username=username,
                    password=password
                )
            ]
        )

        uid = self.repo.add(user)
        user = self.repo.find(uid)
        return user
