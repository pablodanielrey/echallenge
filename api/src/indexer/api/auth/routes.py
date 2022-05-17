from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from .use_cases import models

from .repository import exceptions

from ..jwt.deps import get_jwt_token
from . import deps, schemas
from . import use_cases


router = APIRouter()

@router.get("/admin", response_model=schemas.AdminOut)
def generate_admin(um: use_cases.AddAdmin = Depends(deps.get_add_admin)):
    """
    # Endpoint que permite generar un admin para testear la auth.  
     Genera por defecto el usuario **admin** con clave **admin**  
    ### Returns:  
      - id del usuario admin generado (si no existe)  
     """
    try:
      # user = um.handle(name="admin", 
      #                   lastname="admin", 
      #                   email="admin@gmail.com", 
      #                   username="admin",
      #                   password="admin")
      # return schemas.AdminOut(id=user, username='admin', password='admin')

      user: models.UserWithCredentials = um.handle()
      return schemas.AdminOut(id=user.id, username=user.credentials[0].username, password=user.credentials[0].password)

    except exceptions.IntegrityError as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e    


# @router.post('/users', dependencies=[Depends(get_jwt_token)], response_model=schemas.UserIdOut)
@router.post('/users', response_model=schemas.UserOut)
def create_users(user: schemas.UserIn, 
                 um: use_cases.CreateUser = Depends(deps.get_create_users)):
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

    except exceptions.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e


# @router.get('/users', dependencies=[Depends(get_jwt_token)], response_model=schemas.UsersListOut)
@router.get('/users', response_model=schemas.UsersListOut)
def get_users(skip: Optional[int] = 0,
              limit: Optional[int] = 100,
              um: use_cases.GetUsers = Depends(deps.get_users)):
    """
    # Endpoint de lista de usuarios  
    ### Arguments:
      - skip: indice inicial de la lista de usuarios
      - limit: cantidad de usuarios a obtener  
    ### Returns:
      - lista de usuarios
    """
    # users = um.get_users(skip, limit)
    users = um.handle()
    rusers = [schemas.UserOut(**u.dict()) for u in users]
    return schemas.UsersListOut(skip=skip, limit=limit, size=len(rusers), users=rusers)
