# import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_db_connection: str
    jwt_key: str
    jwt_algo: str
    jwt_issuer: str
    jwt_audience: str
    jwt_expire: int
