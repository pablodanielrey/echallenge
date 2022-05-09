from . import DB
from .models import UsersManager
from .settings import DBSettings


def get_users_manager():
    settings = DBSettings()
    db = DB(settings.db_connection)
    um = UsersManager(db)
    return um
