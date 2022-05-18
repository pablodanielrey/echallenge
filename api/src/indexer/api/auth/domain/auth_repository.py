from typing import Protocol
from uuid import UUID

from .models import UserWithCredentials


class AuthRepository(Protocol):
    """
    Repositorio de usaurios e información de credenciales.
    """

    def add(self, user: UserWithCredentials) -> UUID:
        
        ...

    def find(self, user_id: UUID) -> UserWithCredentials:
        ...

    def find_by_username(self, username: str) -> UserWithCredentials:
        """
        Busca un usuario por username.
        Raises:
            UserNotFound - en el caso de que no se encuentre el usuario
        """
        ...    

    def find_all(self, skip: int = 0, limit: int = 100) -> list[UserWithCredentials]:
        ...


