
import contextlib
from uuid import UUID
from passlib.hash import pbkdf2_sha256

from typing import Any, Generator

from sqlalchemy import create_engine, exc, select
from sqlalchemy.orm import Session, selectinload


from . import Repository, entities, exceptions

from ..use_cases.models import User, UserWithCredentials




class Hasher:

    def hash(self, password: str):
        hash = pbkdf2_sha256.hash(password)
        return hash


class AuthSession:
    """
    Implementa CRUD de las entidades del repositorio.
    """
    
    def __init__(self, session):
        self.session = session
        self.hasher = Hasher()

    def commit(self):
        self.session.commit()

    def add_user(self, user: UserWithCredentials) -> UUID:
        """
        Agrega un usuario y sus credenciales a la base
        Returns:
            UUID: id del usuario recién creado
        """
        try:
            self.session.begin()
            euser = entities.User(**user.dict(exclude={'credentials'}))
            self.session.add(euser)

            for creds in user.credentials:
                eauth = entities.Auth(username=creds.username, 
                            password=self.hasher.hash(creds.password), 
                            user=euser)
                self.session.add(eauth)

            self.session.flush()
            return euser.id

        except exc.IntegrityError as e:
            raise exceptions.IntegrityError() from e


    def get_users(self) -> list[User]:
        """
        Obtiene una lista de usuarios de la base.
        Returns:
            Lista de usuarios con sus credenciales, ordenados por el primer nombre
        """
        stmt = select(entities.User).options(selectinload(entities.User.credentials)).order_by(entities.User.name)
#         if skip:
#             stmt = stmt.offset(skip)
#         if limit:
#             stmt = stmt.limit(limit)
        users = [UserWithCredentials.from_orm(u) for u, in self.session.execute(stmt).all()]
        return users



class AuthRepository(Repository):

    def __init__(self, db_conn: str):
        self.engine = create_engine(db_conn, echo=False)

    def __del__(self):
        if hasattr(self, "engine") and self.engine:
            self.engine.dispose()

    def init_repository(self):
        entities.Base.metadata.create_all(self.engine)

    def clear_repository(self):
        entities.Base.metadata.drop_all(self.engine)

    @contextlib.contextmanager
    def session(self) -> Generator[AuthSession, None, None]:
        session = Session(self.engine, future=True)
        auth_session = AuthSession(session)
        try:
            yield auth_session
        finally:
            session.close()
