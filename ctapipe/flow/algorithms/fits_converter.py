from ctapipe.core import Component
from ctapipe.core.traits import Unicode

from fitsconverter import recoEventsFileToFits


class FitsConverter(Component):
    output_file = Unicode(help='output fits file').tag(config=True)

    def init(self):
        return True

    def run(self, filename):
        recoEventsFileToFits(filename, self.output_file)
        return self.output_file

    def finish(self):
        pass
