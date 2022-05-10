from fastapi import Depends

from . import settings, models

from indexer.vehicles import models as v_models, db as v_db


def _get_config():
    return settings.Settings()


def get_vehicles_manager(config: settings.Settings = Depends(_get_config)):
    db = v_db.DB(config.vehicles_db_connection)
    vm = v_models.VehiclesManager(db)
    return vm


def get_alerts_manager(config: settings.Settings = Depends(_get_config)):
    am = models.AlertsManager(broker_url=config.kafka_broker_url,
                              topic=config.alerts_topic)
    return am
