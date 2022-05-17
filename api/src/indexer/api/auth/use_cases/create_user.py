
from typing import Union, Any
from ..repository.auth import AuthRepository

from . import UseCase, models

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

        with self.repo.session() as session:
            uid = session.add_user(user)
            session.commit()

        user.id = uid
        return user