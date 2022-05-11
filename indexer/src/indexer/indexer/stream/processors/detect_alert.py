from kafka.consumer.fetcher import ConsumerRecord

from ..processor import StreamProcessor, Record

class DetectAlert(StreamProcessor):
    """
        Detecta si el stream contiene un evento para el cual se debe generar una alerta
        Returns:
          - True = se detecto una alerta y se debe continuar con el procesamiento
          - False = no se detecto una alerta. no hay nada mas que hacer.
    """
    def __init__(self, category: str):
        self.category = category

    def start(self):
        pass

    def process_event(self, detection: Record) -> bool:
        alert: bool = self.category == detection.value["Category"]
        return alert