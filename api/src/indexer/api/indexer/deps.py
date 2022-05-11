from fastapi import Depends

from . import settings, models

from indexer.vehicles import models as v_models


def _get_config():
    return settings.Settings()


def get_vehicles_manager(config: settings.Settings = Depends(_get_config)) -> v_models.VehiclesManager:
    """
        quick and dirty. obtengo el manager de vehículos. 
        TODO: cambiar este código por un patrón correcto. (Factory o del estilo) - #codesmell
    """
    con = config.vehicles_db_connection
    if con.startswith('postgresql'):
        from indexer.pgvehicles import db, models as pgmodels
        pgdb = db.DB(con)
        return pgmodels.VehiclesManager(pgdb)

    elif con.startswith('mongo'):
        from indexer.mvehicles import db, models as mmodels
        mdb = db.DB(con)
        return mmodels.VehiclesManager(mdb)

    raise Exception('no se conoce el tipo de base de datos')


def get_alerts_manager(config: settings.Settings = Depends(_get_config)):
    am = models.AlertsManager(broker_url=config.kafka_broker_url,
                              topic=config.alerts_topic)
    return am
