import threading
import os
from ctapipe.core import Component
from ctapipe.core.traits import (
    traits_expand_path,
    traits_expects_directory,
    Unicode,
    validate,
)


class ListProducerProcess(Component):

    source_dir = Unicode('/tmp', help='directory containing data files').tag(
        config=True)

    @validate('source_dir')
    @traits_expand_path
    @traits_expects_directory
    def _check_source_dir(self, proposal):
        return proposal['value']

    def init(self):
        self.log.info('----- ListProducerProcess init  source_dir {}'.format(self.source_dir))
        return True

    def run(self):
        self.log.info('--- {} start ---'.format(threading.get_ident()))
        for input_file in os.listdir(self.source_dir):
            self.log.info('--- ListProducerProcess send  {} ---'.format(self.source_dir + "/" + input_file))
            for connection in self.connections:
                yield (self.source_dir + "/" + input_file, connection)

    def finish(self):
        self.log.info('--- {} finish ---'.format(threading.get_ident()))
