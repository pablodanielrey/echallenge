
from typing import Protocol, Union, Any

class UseCase(Protocol):

    def handle(self, *args, **kw) -> Union[list[Any], Any, None]:
        pass


from .add_admin import AddAdmin
from .get_users import GetUsers
from .create_user import CreateUser
from .login import Login

__all__ = [
    'AddAdmin',
    'GetUsers',
    'CreateUser',
    'Login'
]