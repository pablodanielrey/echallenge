from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import deps as auth_deps
from ..auth.use_cases import models as auth_models
from ..auth.repository import exceptions as auth_exceptions
from . import schemas, models, deps, exceptions


router = APIRouter()


# @router.post('/login', response_model=schemas.Token)
# def oauth2_token(form_data: OAuth2PasswordRequestForm = Depends(),
#                  jwt_manager: models.JWTManager = Depends(deps.get_jwt_manager), 
#                  um: auth_models.UsersManager = Depends(auth_deps.get_users_manager)):
#     """
#     # Endpoint que permite loguearse para obtener un token jwt  
#     ### Arguments:
#       - usuario: nombre de usuario a autentificar
#       - password: clave del usuario a verificar
#     ### Returns:
#       - token jwt
#     """
#     try:
#         user = um.login(form_data.username, form_data.password)
#         payload = {
#             "sub": f"username:{form_data.username}"
#         }
#         u = schemas.UserToken.from_orm(user)
#         payload.update(u.dict())
#         token = jwt_manager.encode_jwt(payload)
#         return schemas.Token(access_token=token, token_type="bearer")

#     except auth_exceptions.UserNotFound as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e

#     except exceptions.JWTException as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e
