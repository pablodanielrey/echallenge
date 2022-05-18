from typing import Optional
from uuid import UUID
from passlib.hash import pbkdf2_sha256

from pydantic import BaseModel

from .exceptions import CredentialsNotFound, IncorrectCredentials

class Hasher:
    """
    Implementa el hash de las claves dentro de la base.
    Por ahora es una clase con métodos de clase. después veo la mejor forma de abstracción dentro del sistema.
    Nota: es usada solo dentro de esta capa.
    """

    @classmethod
    def hash(cls, password: str) -> str:
        hash = pbkdf2_sha256.hash(password)
        return hash

    @classmethod
    def verify(cls, password: str, hash: str):
        if pbkdf2_sha256.verify(password, password):
            raise IncorrectCredentials()



class Credentials(BaseModel):
    username: str
    password: str
    valid: bool = True

    class Config:
        orm_mode = True

    def is_valid(self):
        return self.valid

    def verify(self, password: str):
        if not pbkdf2_sha256.verify(password, self.password):
            raise IncorrectCredentials()
        

class User(BaseModel):
    id: Optional[UUID] = None
    name: str
    lastname: str
    email: Optional[str] = None

    class Config:
        orm_mode = True


class UserWithCredentials(User):
    """
    Representa un usuario y sus credenciales.
    En DDD sería el root agregate
    """
    credentials: list[Credentials] = []

    class Config:
        orm_mode = True

    def _find_valid_credential(self) -> Credentials:
        for credential in self.credentials:
            if credential.is_valid():
                return credential
        raise CredentialsNotFound()

    def verify_password(self, password: str):
        credentials = self._find_valid_credential()
        credentials.verify(password)




# class UsersManager:

#     def __init__(self, db: DB):
#         self.db = db
#         self.db.generate_db()

#     def _hash_password(self, password: str):
#         hash = pbkdf2_sha256.hash(password)
#         return hash

#     def add_user(self, name: str, lastname: str, email: str, username: str, password: str) -> str:
#         try:
#             with self.db.session() as session, session.begin():
#                 user = entities.User(name=name, 
#                             lastname=lastname, 
#                             email=email)
#                 auth = entities.Auth(username=username, 
#                             password=self._hash_password(password), 
#                             user=user)
#                 # auth.user = user
#                 # auth.password = self._hash_password(auth.password)
#                 session.add(user)
#                 session.add(auth)
#                 session.flush()
#                 return str(user.id)

#         except exc.IntegrityError as e:
#             raise IntegrityError() from e


#     def get_users(self, skip: Optional[int] = None, limit: Optional[int] = None) -> list[User]:
#         stmt = select(entities.User).options(selectinload(entities.User.credentials)).order_by(User.name)
#         if skip:
#             stmt = stmt.offset(skip)
#         if limit:
#             stmt = stmt.limit(limit)
#         with self.db.session() as session:
#             users = [u for u, in session.execute(stmt).all()]
#         return users

#     def login(self, username: str, password: str) -> User:
#         stmt = select(entities.Auth).where(entities.Auth.username == username, entities.Auth.active)
#         print(stmt)
#         with self.db.session() as session:
#             rauth = session.execute(stmt).one_or_none()
#             if not rauth:
#                 raise UserNotFound()
#             auth = rauth[0]
#             print(auth.password)
#             if not pbkdf2_sha256.verify(password, auth.password):
#                 raise IncorrectCredentials()
#             return auth.user