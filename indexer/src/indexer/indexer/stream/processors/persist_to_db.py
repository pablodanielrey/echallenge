
from indexer.vehicles import models

from ..processor import StreamProcessor, Record

class PersistToDB(StreamProcessor):

    def __init__(self, vm: models.VehiclesManager):
        self.vm = vm

    def process_event(self, detection_event: Record) -> bool:
        # logging.warn(f"agregando la detección {detection.value} a la base")
        # detection = {"timestamp": detection_event.timestamp, **detection_event.value}
        self.vm.add_detection(timestamp=detection_event.timestamp, **detection_event.value)
        return True

