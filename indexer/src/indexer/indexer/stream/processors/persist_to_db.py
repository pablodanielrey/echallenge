
from indexer.vehicles import models

from ..processor import StreamProcessor, Record

class PersistToDB(StreamProcessor):
    """
    Persiste los eventos de detección en la db.
    Este es el procesador que inicia la cadena de procesamiento.
    Returns:  
      - True = se continua con el procesamiento del evento.
    """

    def __init__(self, vm: models.VehiclesManager):
        self.vm = vm

    def start(self):
        pass

    def process_event(self, detection_event: Record) -> bool:
        self.vm.add_detection(timestamp=detection_event.timestamp, **detection_event.value)
        return True

