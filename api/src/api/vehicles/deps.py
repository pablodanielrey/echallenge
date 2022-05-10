from fastapi import Depends

from api.db import DB
from . import settings, models


def _get_config():
    return settings.Settings()


def get_vehicles_manager(config: settings.Settings = Depends(_get_config)):
    db = DB(config.vehicles_db_connection)
    vm = models.VehiclesManager(db)
    return vm


def get_alerts_manager(config: settings.Settings = Depends(_get_config)):
    am = models.AlertsManager(broker_url=config.kafka_broker_url,
                              topic=config.alerts_topic)
    return am
