
import contextlib
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DB:

    def __init__(self, db_conn: str):
        self.engine = create_engine(db_conn, echo=False)

    def __del__(self):
        if hasattr(self, "engine") and self.engine:
            self.engine.dispose()

    def generate_db(self):
        Base.metadata.create_all(self.engine)

    def drop_db(self):
        Base.metadata.drop_all(self.engine)

    @contextlib.contextmanager
    def session(self):
        session = Session(self.engine, future=True)
        try:
            yield session
        finally:
            session.close()

    # @staticmethod
    # def from_dict(cls: type[Base], data: dict[str, Any]):
    #     """
    #         Método utilitario para parsear dics a entidades de sqlalchemy.
    #         El case de las claves no es importante ya que se lleva todo a lower. (year == Year)
    #     """
    #     columns_names = {c.name.lower() for c in cls.__table__.columns}
    #     filtered_dict = {k.lower(): v for (k, v) in data.items() if k.lower() in columns_names}
    #     return cls(**filtered_dict)
