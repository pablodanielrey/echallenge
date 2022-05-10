from fastapi import Depends

from api.db import DB
from . import models, settings


def get_users_manager():
    config = settings.Settings()
    db = DB(config.auth_db_connection)
    um = models.UsersManager(db)
    return um
