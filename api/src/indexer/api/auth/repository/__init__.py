
from typing import Protocol, Generator


class Repository(Protocol):


    def init_repository(self):
        ...


    def clear_repository(self):
        ...


    def session(self) -> Generator:
        """
        Genera una sessión para trabajar con el repositorio
        Returns:
            Sesión de trabajo dentro de la cual el repo es funcional
        """
        ...




from .auth import AuthRepository, AuthSession

__all__ = [
    'AuthRepository',
    'AuthSession'
]