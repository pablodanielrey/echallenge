
import logging
import contextlib
from uuid import UUID

from typing import Any

from sqlalchemy import create_engine, exc, select
from sqlalchemy.orm import Session, selectinload


#las importo asi y no relativas porque podría separarlas a un package.
from indexer.api.auth.domain import exceptions as domain_exceptions
from indexer.api.auth.domain.auth_repository import AuthRepository
from indexer.api.auth.domain.models import UserWithCredentials, Hasher

from . import entities, exceptions


class AuthRepository(AuthRepository):

    def __init__(self, db_conn: str, hasher: Hasher):
        self.engine = create_engine(db_conn, echo=False)
        self.hasher = hasher

    def __del__(self):
        if hasattr(self, "engine") and self.engine:
            self.engine.dispose()

    def init_repository(self):
        entities.Base.metadata.create_all(self.engine)

    def clear_repository(self):
        entities.Base.metadata.drop_all(self.engine)


    @contextlib.contextmanager
    def _session(self):
        session = Session(self.engine, future=True)
        try:
            yield session
        finally:
            session.close()


    def add(self, user: UserWithCredentials) -> UUID:
        try:
            with self._session() as session, session.begin():
                euser = entities.User(**user.dict(exclude={'credentials'}))
                session.add(euser)

                for creds in user.credentials:
                    eauth = entities.Auth(username=creds.username, 
                                password=self.hasher.hash(creds.password), 
                                user=euser)
                    session.add(eauth)

                session.flush()
                return euser.id

        except exc.IntegrityError as e:
            raise domain_exceptions.DupplicatedUser() from e


    def find(self, user_id: UUID) -> UserWithCredentials:
        stmt = select(entities.User).where(entities.User.id == user_id).options(selectinload(entities.User.credentials))
        with self._session() as session:
            ruser = session.execute(stmt).one_or_none()
            if not ruser:
                raise domain_exceptions.UserNotFound()
            user = UserWithCredentials.from_orm(ruser[0])
        return user



    def find_by_username(self, username: str) -> UserWithCredentials:
        # stmt = select(entities.Auth).where(entities.Auth.username == username, entities.Auth.active)
        # stmt = select(entities.User).select_from.where(entities.Auth.username == username).options(selectinload(entities.User.credentials))
        stmt = select(entities.User).select_from(entities.Auth).join(entities.Auth.user).where(entities.Auth.username == username).options(selectinload(entities.User.credentials))
        with self._session() as session:
            rauth = session.execute(stmt).one_or_none()
            if not rauth:
                raise domain_exceptions.UserNotFound()
            user = UserWithCredentials.from_orm(rauth[0])
        return user


    def find_all(self, skip: int = 0, limit: int = 100) -> list[UserWithCredentials]:
        """
        Obtiene una lista de usuarios de la base.
        Returns:
            Lista de usuarios con sus credenciales, ordenados por el primer nombre
        """
        stmt = select(entities.User).options(selectinload(entities.User.credentials)).order_by(entities.User.name)
        if skip:
            stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)
        with self._session() as session:
            users = [UserWithCredentials.from_orm(u) for u, in session.execute(stmt).all()]
        return users

