from ctapipe.core import Component


class CountWord(Component):
    """Add class represents a Stage for pipeline.
    It returns inverted value of received value
    """
    def init(self):
        self.log.debug("--- CountWord init ---")
        return True

    def run(self, filepath):
        if filepath:
            self.log.debug("countWord receive {}".format(filepath))
            with open(filepath) as f:
                return len(f.read())


    def finish(self):
        self.log.debug("--- CountWord finish ---")
