from traitlets import Unicode
from traitlets import List
from ctapipe.flow.algorithms.in_out_process import InOutProcess



class PTableHillasSvdSetSplitter(InOutProcess):

    exe = Unicode(help='executable').tag(
        config=True)
    options = List(help='executable option').tag(
        config=True)

    def init(self):
        super().init(self.exe, self.options)
