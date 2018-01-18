from traitlets import Unicode
from traitlets import List
from ctapipe.flow.algorithms.in_out_process import InOutProcess



class PTableHillasSVSplitter(InOutProcess):

    exe = Unicode(help='executable').tag(
        config=True)
    options = List(help='executable option').tag(
        config=True)
    output_dir = Unicode("/tmp", help='executable').tag(
        config=True)
    out_extension = 'ptabhillassv'


    def init(self):
        super().init(self.exe, self.options,
                     output_dir=self.output_dir, out_extension=self.out_extension)
