from traitlets import Unicode
from traitlets import List
from ctapipe.flow.algorithms.in_out_process import InOutProcess



class PTimeHillasSvdSet2Precoevent(InOutProcess):

    exe = Unicode(help='executable').tag(
        config=True, allow_none=False)
    options = List(help='executable option').tag(
        config=True, allow_none=True)

    def init(self):
        super().init(self.exe, self.options, out_extension="precoevent")
