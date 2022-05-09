from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# from epic.jwt.fastapi import get_jwt_manager
# from epic.jwt.models import JWTManager

# from auth.db import auth
# from auth.api.settings import get_users_manager
# from auth.api import schemas

from api.schemas.jwt import Token
from api.schemas.auth import User
from api.jwt.models import JWTManager
from api.jwt.deps import get_jwt_manager
from api.jwt.exceptions import JWTException
from api.db.deps import get_users_manager
from api.db.models import UsersManager
from api.db.exceptions import UserNotFound

router = APIRouter()


@router.post('/login', response_model=Token)
def oauth2_token(form_data: OAuth2PasswordRequestForm = Depends(),
                 jwt_manager: JWTManager = Depends(get_jwt_manager), 
                 um: UsersManager = Depends(get_users_manager)):
    """
    ## Login para obtener un token jwt
    """
    try:
        user = um.login(form_data.username, form_data.password)
        payload = {
            "sub": f"username:{form_data.username}"
        }
        u = User.from_orm(user)
        payload.update(u.dict())
        token = jwt_manager.encode_jwt(payload)
        return Token(access_token=token, token_type="bearer")

    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e

    except JWTException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e
