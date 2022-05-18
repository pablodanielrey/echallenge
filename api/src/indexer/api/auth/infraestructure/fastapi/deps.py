from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

from indexer.api.auth.domain import models
from indexer.api.auth import application

from indexer.api.jwt.services import JWTManager
from indexer.api.jwt.exceptions import JWTException

from .settings import Settings
from ..repo.auth_repository import AuthRepository


def get_settings():
    config = Settings()
    return config


def get_repo(config: Settings = Depends(get_settings)):
    repo = AuthRepository(config.auth_db_connection, hasher=models.Hasher())
    return repo


def get_add_admin(repo: AuthRepository = Depends(get_repo)):
    # config = settings.Settings()
    # repo = AuthRepository(config.auth_db_connection)
    return application.AddAdmin(repo)


def get_users(repo: AuthRepository = Depends(get_repo)):
    return application.GetUsers(repo)


def get_create_users(repo: AuthRepository = Depends(get_repo)):
    return application.CreateUser(repo)


def get_login(repo: AuthRepository = Depends(get_repo)):
    return application.Login(repo)


async def get_jwt_manager(settings: Settings = Depends(get_settings)):
    return JWTManager(settings.jwt_key,
                      settings.jwt_algo,
                      settings.jwt_audience,
                      settings.jwt_issuer,
                      settings.jwt_expire)


oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_jwt_token(token: str = Depends(oauth_scheme), jwt_manager: JWTManager = Depends(get_jwt_manager)):
    try:
        payload = jwt_manager.decode_jwt(token)
    except JWTException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

