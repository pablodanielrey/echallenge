from pydantic import BaseSettings


class JWTSettings(BaseSettings):
    jwt_key: str
    jwt_algo: str
    jwt_issuer: str
    jwt_audience: str
    jwt_expire: int
