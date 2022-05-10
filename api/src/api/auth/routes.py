from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from api.jwt.deps import get_jwt_token
from . import deps, models, exceptions, schemas


router = APIRouter()

@router.get("/admin")
def generate_admin(um: models.UsersManager = Depends(deps.get_users_manager)):
    try:
        uid = um.add_user(name="admin", 
                          lastname="admin", 
                          email="admin@gmail.com", 
                          username="admin",
                          password="admin")
        return schemas.UserId(id=str(uid))
    except Exception:
        return schemas.UserId(id="1")    


@router.post('/users', dependencies=[Depends(get_jwt_token)])
def create_users(user: schemas.UserWithCredentials, 
                 um: models.UsersManager = Depends(deps.get_users_manager)):
    """
    ## Endpoint de creación de usuarios
    """
    try:
        user_data = user.flatten_dict()
        uid = um.add_user(**user_data)
        return schemas.UserId(id=str(uid))

    except exceptions.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e


@router.get('/users', dependencies=[Depends(get_jwt_token)])
def get_users(skip: Optional[int] = 0,
              limit: Optional[int] = 100,
              um: models.UsersManager = Depends(deps.get_users_manager)):
    """
    ## Endpoint de lista de usuarios
    """
    users = um.get_users(skip, limit)
    return users

