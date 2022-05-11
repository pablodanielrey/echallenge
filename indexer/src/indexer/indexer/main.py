import logging
import os

from indexer.vehicles.models import VehiclesManager

from .settings import Settings

from .models import Indexer
from .stream.processors import DetectAlert, PersistToDB, PublishAlert
from .stream.listener import StreamListener


def get_vehicles_manager(settings: Settings) -> VehiclesManager:
    """
        quick and dirty. obtengo el manager de vehículos. 
        TODO: cambiar este código por un patrón correcto. (Factory o del estilo) - #codesmell
    """
    con = settings.vehicles_db_connection
    if con.startswith('postgresql'):
        from indexer.pgvehicles import db, models
        pgdb = db.DB(con)
        return models.VehiclesManager(pgdb)

    elif con.startswith('mongo'):
        from indexer.mvehicles import db, models
        mdb = db.DB(con)
        return models.VehiclesManager(mdb)

    raise Exception('no se conoce el tipo de base de datos')


def start():
    logging.getLogger().setLevel(logging.WARNING)
    logging.info("iniciando el indexer y los processors")

    settings = Settings()

    listener = StreamListener(settings.kafka_broker_url, settings.detections_topic)
    detect_alert = DetectAlert(settings.suspicious_vehicle)

    vm = get_vehicles_manager(settings)
    persist_to_db = PersistToDB(vm)

    publish_to_api = PublishAlert(settings.kafka_broker_url, settings.alerts_topic)

    indexer = Indexer(listener, [persist_to_db, detect_alert, publish_to_api])
    indexer.start()


if __name__ == '__main__':
    start()
