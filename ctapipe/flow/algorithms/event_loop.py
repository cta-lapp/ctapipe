from ctapipe.core import Component
from ctapipe.io import event_source



class EventLoop(Component):


    def init(self):
        self.log.debug("--- EventLoop init ---")
        return True

    def run(self, filename):
        with event_source(filename) as source:
            # with EventSourceFactory.produce(filename):
            for event in source:
                yield(event)

    def finish(self):
        self.log.debug("--- EventLoop finish ---")
