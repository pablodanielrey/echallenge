from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

# from epic.jwt.fastapi import get_jwt_token

# from auth.db import auth
# from auth.db.exceptions import IntegrityError
# from auth.api.settings import get_users_manager
# from auth.api.schemas import User, UserWithCredentials

from api.jwt.deps import get_jwt_token
from api.db.deps import get_users_manager
from api.db.models import UsersManager
from api.db.exceptions import IntegrityError
from api.schemas.auth import UserWithCredentials, UserId

router = APIRouter()

@router.get("/admin")
def generate_admin(um: UsersManager = Depends(get_users_manager)):
    try:
        uid = um.add_user(name="admin", 
                    lastname="admin", 
                    email="admin@gmail.com", 
                    username="admin",
                    password="admin")
        return UserId(id=str(uid))
    except Exception:
        return UserId(id="1")    


@router.post('/users', dependencies=[Depends(get_jwt_token)])
def create_users(user: UserWithCredentials, 
                       um: UsersManager = Depends(get_users_manager)):
    """
    ## Endpoint de creación de usuarios
    """
    try:
        user_data = user.flatten_dict()
        uid = um.add_user(**user_data)
        return UserId(id=str(uid))

    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from e


@router.get('/users', dependencies=[Depends(get_jwt_token)])
def get_users(skip: Optional[int] = 0,
              limit: Optional[int] = 100,
              um: UsersManager = Depends(get_users_manager)):
    """
    ## Endpoint de lista de usuarios
    """
    users = um.get_users(skip, limit)
    return users

