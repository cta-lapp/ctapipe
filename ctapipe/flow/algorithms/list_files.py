import os
from ctapipe.core import Component
from traitlets import Unicode


class ListFiles(Component):

    source_dir = Unicode('/tmp', help='directory containing data files').tag(config=True)
    extension = Unicode('*', help='filter file extension').tag(config=True)

    def init(self):
        self.log.info('----- ListFiles 1 init  source_dir {}'.format(self.source_dir))
        return True

    def run(self):
        self.log.info('ListFiles --- start ---')
        files_list = [f for f in os.listdir(self.source_dir) if
                      os.path.isfile(os.path.join(self.source_dir, f)) and
                      f.split('.')[-1] == self.extension]

        for input_file in files_list:
            self.log.info('--- ListProducerProcess send  {} ---'.format(self.source_dir + "/" + input_file))
            yield self.source_dir + "/" + input_file

    def finish(self):
        self.log.info('--- ListFiles finish ---')
