from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import schemas as auth_schemas
from ..auth import deps as auth_deps
from ..auth import models as auth_models
from ..auth import exceptions as auth_exceptions
from . import schemas, models, deps, exceptions


router = APIRouter()


@router.post('/login', response_model=schemas.Token)
def oauth2_token(form_data: OAuth2PasswordRequestForm = Depends(),
                 jwt_manager: models.JWTManager = Depends(deps.get_jwt_manager), 
                 um: auth_models.UsersManager = Depends(auth_deps.get_users_manager)):
    """
    ## Login para obtener un token jwt
    """
    try:
        user = um.login(form_data.username, form_data.password)
        payload = {
            "sub": f"username:{form_data.username}"
        }
        u = auth_schemas.User.from_orm(user)
        payload.update(u.dict())
        token = jwt_manager.encode_jwt(payload)
        return schemas.Token(access_token=token, token_type="bearer")

    except auth_exceptions.UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e

    except exceptions.JWTException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e
