import os
from ctapipe.core import Component
from traitlets import Unicode


class ListProducerProcess(Component):

    source_dir = Unicode('/tmp', help='directory containing data files').tag(config=True)

    def init(self):
        self.log.info('----- ListProducerProcess 1 init  source_dir {}'.format(self.source_dir))
        return True

    def run(self):
        self.log.info('ListProducerProcess --- start ---')
        files_list = [f for f in os.listdir(self.source_dir) if
                      os.path.isfile(os.path.join(self.source_dir, f))]


        # Inform consumer about number of input to wait before starting
        msg_for_consumer = ('expected', len(files_list))
        self.log.info('ListProducerProcess --- send {} to WaitAndTotal --- '.format(msg_for_consumer))
        yield(msg_for_consumer, 'WaitAndTotal')

        for input_file in files_list:
            self.log.info('--- ListProducerProcess send  {} ---'.format(self.source_dir + "/" + input_file))
            yield(self.source_dir + "/" + input_file, 'CountWord')

    def finish(self):
        self.log.info('--- ListProducerProcess finish ---')
