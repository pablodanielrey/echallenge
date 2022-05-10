# import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_db_connection: str
