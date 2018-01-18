from ctapipe.core import Component
from traitlets import Unicode
from time import sleep


class StringWriter(Component):

    """`StringWriter` class represents a Stage or a Consumer for pipeline.
        It writes received objects to file
    """
    filename = Unicode('/tmp/test.txt', help='output filename').tag(
        config=True, allow_none=True)

    def init(self):
        self.file = open(self.filename, 'w')
        self.log.debug("--- StringWriter init filename {}---".format(self.filename))
        return True

    def run(self, obj):
        self.file.write(str(obj) + "\n")
        self.log.debug('StringWriter write {}'.format(obj))

    def finish(self):
        self.file.close()
        self.log.debug("--- StringWriter finish---")
