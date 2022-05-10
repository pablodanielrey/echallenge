
import contextlib
import uuid
from typing import Any

from pydantic import BaseModel

import pymongo


class DB:

    def __init__(self, db_conn: str):
        self.client = pymongo.MongoClient(db_conn, uuidRepresentation='standard')
        self.generate_db()

    def __del__(self):
        try:
            self.client.close()
        except Exception:
            pass

    def generate_db(self):
        self.db = self.client.vehicles
        self.detections = self.db.detections
        self.detections.create_index([("id", pymongo.ASCENDING)], unique=True)
        self.detections.create_index([("make", pymongo.ASCENDING)], unique=False)

    def drop_db(self):
        self.client.drop_database("vehicles")

    @contextlib.contextmanager
    def session(self):
        try:
            yield self.db
        finally:
            pass

    @staticmethod
    def from_dict(cls: type[BaseModel], data: dict[str, Any]) -> BaseModel:
        """
            Método utilitario para parsear dics a entidades de sqlalchemy.
            El case de las claves no es importante ya que se lleva todo a lower. (year == Year)
        """
        filtered_dict = {k.lower(): v for (k, v) in data.items() if k.lower() in cls.__fields__.keys()}
        if "id" not in filtered_dict:
            filtered_dict["id"] = uuid.uuid4()
        return cls(**filtered_dict)

