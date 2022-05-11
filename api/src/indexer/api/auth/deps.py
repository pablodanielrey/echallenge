from fastapi import Depends

from . import models, settings
from .db import DB


def get_users_manager():
    config = settings.Settings()
    db = DB(config.auth_db_connection)
    um = models.UsersManager(db)
    return um
