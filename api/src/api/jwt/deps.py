
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

from .settings import JWTSettings
from .exceptions import JWTException
from .models import JWTManager


async def get_jwt_manager():
    settings = JWTSettings()
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

