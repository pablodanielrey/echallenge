# import os
from pydantic import BaseSettings


class DBSettings(BaseSettings):
    db_connection: str

