from time import sleep

from ctapipe.core.traits import (
    traits_expand_path,
    Unicode,
)
from ctapipe.core import Component


class StringWriter(Component):

    """`StringWriter` class represents a Stage or a Consumer for pipeline.
        It writes received objects to file
    """
    filename = Unicode('/tmp/test.txt', help='output filename').tag(
        config=True)

    def init(self):
        self.file = open(self.filename, 'w')
        self.log.info("--- StringWriter init filename {}---".format(self.filename))
        return True

    def run(self, object):
        self.file.write(str(object) + "\n")
        self.log.debug('StringWriter write {}'.format( object))

    def finish(self):
        self.file.close()
        self.log.debug("--- StringWriter finish---")

    @validate('filename')
    @traits_expand_path
    def _check_filename(self, proposal):
        return proposal['value']
