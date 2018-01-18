from traitlets import Unicode
from traitlets import List
from ctapipe.flow.algorithms.in_out_process import InOutProcess



class PTableHillasSV2PTimeHillasSV(InOutProcess):

    exe = Unicode(help='executable').tag(
        config=True)
    options = List(help='executable option').tag(
        config=True)
    output_dir = Unicode("/tmp", help='executable').tag(
        config=True)
    out_extension = 'ptimehillassv'



    def init(self):
        super().init(self.exe, self.options,
                     output_dir=self.output_dir, out_extension=self.out_extension)
