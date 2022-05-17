from fastapi import Depends
from .use_cases import models

from indexer.api.auth import use_cases

from . import settings
from .repository import AuthRepository


# def get_users_manager():
#     config = settings.Settings()
#     db = AuthRepository(config.auth_db_connection)
#     um = models.UsersManager(db)
#     return um


def get_settings():
    config = settings.Settings()
    return config


def get_repo(config: settings.Settings = Depends(get_settings)):
    repo = AuthRepository(config.auth_db_connection)
    return repo


def get_add_admin(repo: AuthRepository = Depends(get_repo)):
    # config = settings.Settings()
    # repo = AuthRepository(config.auth_db_connection)
    return use_cases.AddAdmin(repo)


def get_users(repo: AuthRepository = Depends(get_repo)):
    return use_cases.GetUsers(repo)


def get_create_users(repo: AuthRepository = Depends(get_repo)):
    return use_cases.CreateUser(repo)    