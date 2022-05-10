
from kafka.consumer.fetcher import ConsumerRecord

Record = ConsumerRecord

class StreamProcessor:

    def start(self):
        pass

    def process_event(self, detection: Record) -> bool:
        return True
