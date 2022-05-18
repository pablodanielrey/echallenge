from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from indexer.api.auth import application
from indexer.api.auth.domain import models, exceptions as domain_exceptions

from indexer.api.jwt import exceptions as jwt_exceptions
from indexer.api.jwt import services as jwt_models

from . import deps
from . import schemas
from ..repo import exceptions as repo_exceptions


router = APIRouter()

@router.get("/admin", response_model=schemas.AdminOut)
def generate_admin(um: application.AddAdmin = Depends(deps.get_add_admin)):
    """
    # Endpoint que permite generar un admin para testear la auth.  
     Genera por defecto el usuario **admin** con clave **admin**  
    ### Returns:  
      - id del usuario admin generado (si no existe)  
     """
    try:
      user: models.UserWithCredentials = um.handle()
      assert user.id is not None
      return schemas.AdminOut(id=user.id, username=user.credentials[0].username, password=user.credentials[0].password)

    except domain_exceptions.DupplicatedUser as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario existente") from e



@router.post('/users',  dependencies=[Depends(deps.get_jwt_token)], response_model=schemas.UserOut)
def create_users(user: schemas.UserIn, 
                 um: application.CreateUser = Depends(deps.get_create_users)):
    """
    # Endpoint de creación de usuarios  
    ### Arguments:  
      - user: usuario con credenciales a crear  
    ### Returns:  
      - id de usuario generado
    """
    try:
        usero = um.handle(**user.dict())
        return schemas.UserOut(**usero.dict())

    except domain_exceptions.DupplicatedUser as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario existente") from e



@router.get('/users', dependencies=[Depends(deps.get_jwt_token)], response_model=schemas.UsersListOut)
def get_users(skip: Optional[int] = 0,
              limit: Optional[int] = 100,
              um: application.GetUsers = Depends(deps.get_users)):
    """
    # Endpoint de lista de usuarios  
    ### Arguments:
      - skip: indice inicial de la lista de usuarios
      - limit: cantidad de usuarios a obtener  
    ### Returns:
      - lista de usuarios
    """
    # users = um.get_users(skip, limit)
    users = um.handle(skip=skip, limit=limit)
    rusers = [schemas.UserOut(**u.dict()) for u in users]
    return schemas.UsersListOut(skip=skip, limit=limit, size=len(rusers), users=rusers)


@router.post('/login', response_model=schemas.Token)
def oauth2_token(form_data: OAuth2PasswordRequestForm = Depends(),
                 jwt_manager: jwt_models.JWTManager = Depends(deps.get_jwt_manager), 
                 um: application.Login = Depends(deps.get_login)):
    """
    # Endpoint que permite loguearse para obtener un token jwt
    # El token es un aspecto de infraestructura, y de seguridad de los endpoints. por eso 
    # lo manejo en la capa de infraestructura en vez de en la capa de aplicación.
    # si pasa a ser un aspecto de apicación posteriomente lo trasladaría a esa capa.
    ### Arguments:
      - usuario: nombre de usuario a autentificar
      - password: clave del usuario a verificar
    ### Returns:
      - token jwt
    """
    try:
        user = um.handle(form_data.username, form_data.password)
        payload = {
            "sub": f"username:{form_data.username}"
        }
        u = schemas.UserToken.from_orm(user)
        payload.update(u.dict())
        token = jwt_manager.encode_jwt(payload)
        return schemas.Token(access_token=token, token_type="bearer")

    except domain_exceptions.UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e

    except jwt_exceptions.JWTException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e

