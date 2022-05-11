from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from ..jwt.deps import get_jwt_token
from . import deps, models, exceptions, schemas


router = APIRouter()

@router.get("/admin", response_model=schemas.UserId)
def generate_admin(um: models.UsersManager = Depends(deps.get_users_manager)):
    """
    # Endpoint que permite generar un admin para testear la auth.  
     Genera por defecto el usuario **admin** con clave **admin**  
    ### Returns:  
      - id del usuario admin generado (si no existe)  
     """
    try:
      user = um.add_user(name="admin", 
                        lastname="admin", 
                        email="admin@gmail.com", 
                        username="admin",
                        password="admin")
      return schemas.UserId(id=user)
    except exceptions.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e    


@router.post('/users', dependencies=[Depends(get_jwt_token)], response_model=schemas.UserId)
def create_users(user: schemas.UserIn, 
                 um: models.UsersManager = Depends(deps.get_users_manager)):
    """
    # Endpoint de creación de usuarios  
    ### Arguments:  
      - user: usuario con credenciales a crear  
    ### Returns:  
      - id de usuario generado
    """
    try:
        # user_data = user.flatten_dict()
        usero = um.add_user(**user.dict())
        return schemas.UserId(id=usero)

    except exceptions.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e


@router.get('/users', dependencies=[Depends(get_jwt_token)], response_model=schemas.UsersList)
def get_users(skip: Optional[int] = 0,
              limit: Optional[int] = 100,
              um: models.UsersManager = Depends(deps.get_users_manager)):
    """
    # Endpoint de lista de usuarios  
    ### Arguments:
      - skip: indice inicial de la lista de usuarios
      - limit: cantidad de usuarios a obtener  
    ### Returns:
      - lista de usuarios
    """
    users = um.get_users(skip, limit)
    return schemas.UsersList(skip=skip, limit=limit, size=len(users), users=users)
