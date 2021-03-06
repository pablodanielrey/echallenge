from typing import Optional
from passlib.hash import pbkdf2_sha256

from sqlalchemy import select, exc
from sqlalchemy.orm import selectinload


from .db import DB
from .entities import User, Auth
from .exceptions import IntegrityError, IncorrectCredentials, UserNotFound
from . import schemas

import logging
logging.getLogger().setLevel(logging.DEBUG)
class UsersManager:

    def __init__(self, db: DB):
        self.db = db
        self.db.generate_db()

    def _hash_password(self, password: str):
        hash = pbkdf2_sha256.hash(password)
        return hash

    def add_user(self, name: str, lastname: str, email: str, username: str, password: str) -> str:
        try:
            with self.db.session() as session, session.begin():
                user = User(name=name, 
                            lastname=lastname, 
                            email=email)
                auth = Auth(username=username, 
                            password=self._hash_password(password), 
                            user=user)
                # auth.user = user
                # auth.password = self._hash_password(auth.password)
                session.add(user)
                session.add(auth)
                session.flush()
                return str(user.id)

        except exc.IntegrityError as e:
            raise IntegrityError() from e

    def get_users(self, skip: Optional[int] = None, limit: Optional[int] = None) -> list[User]:
        stmt = select(User).options(selectinload(User.credentials)).order_by(User.name)
        if skip:
            stmt = stmt.offset(skip)
        if limit:
            stmt = stmt.limit(limit)
        with self.db.session() as session:
            users = [u for u, in session.execute(stmt).all()]
        return users

    def login(self, username: str, password: str) -> User:
        stmt = select(Auth).where(Auth.username == username, Auth.active)
        print(stmt)
        with self.db.session() as session:
            rauth = session.execute(stmt).one_or_none()
            if not rauth:
                raise UserNotFound()
            auth = rauth[0]
            print(auth.password)
            if not pbkdf2_sha256.verify(password, auth.password):
                raise IncorrectCredentials()
            return auth.user