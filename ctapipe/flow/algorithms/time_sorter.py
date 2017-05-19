from traitlets import Unicode
from traitlets import List
from ctapipe.flow.algorithms.in_out_process import InOutProcess



class TimeSorter(InOutProcess):

    exe = Unicode(help='executable').tag(
        config=True, allow_none=False)
    options = List(help='executable option').tag(
        config=True, allow_none=True)
    output_dir=Unicode("/tmp", help='executable').tag(
            config=True)


    def init(self):
        super().init(self.exe, self.options, out_extension="ptimehillassvdset",
                     output_dir=self.output_dir)
