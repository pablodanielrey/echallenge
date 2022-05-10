from .stream import listener, processor

class Indexer:

    def __init__(self,
                 stream_listener: listener.StreamListener,
                 stream_processors: list[processor.StreamProcessor]):

        self.stream_processors = stream_processors
        self.stream_listener = stream_listener
        self.stream_listener.add_procesors(stream_processors)

    def start(self):
        for sp in self.stream_processors:
            sp.start()
        self.stream_listener.start()
        self.stream_listener.process_loop()

