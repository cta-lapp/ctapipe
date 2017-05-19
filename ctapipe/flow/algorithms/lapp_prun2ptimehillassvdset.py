from ctapipe.core import Component
from traitlets import Unicode
from subprocess import Popen
from ctapipe.flow.algorithms.build_command import build_command



class Prun2PtimehillasSvdSet(Component):

    exe = Unicode(help='executable').tag(
        config=True, allow_none=False)

    config_file = Unicode(help='configuration file').tag(
        config=True, allow_none=False)

    cleaningType = Unicode(help='cleaning type').tag(
        config=True, allow_none=True)

    """CalibrationStep` class represents a Stage for pipeline.
        it executes prun2pcalibrun
    """
    def init(self):
        self.log.debug("--- CalibrationStep init ---")
        if self.exe:

            return True
        return False

    def run(self, in_filename):
        if in_filename != None:
            options = ["-c", self.config_file, "--CleaningType", self.cleaningType]
            cmd, output_file = build_command(self.exe,  in_filename,
                                             output_dir=".",
                                             out_extension="ptimehillas",
                                             options=options)
            self.log.info("--- InOutProcess cmd {} --- in_filename {}".format(cmd, in_filename))
            proc = Popen(cmd)
            proc.wait()
            self.log.debug("--- CalibrationStep STOP ---")
            return  output_file

    def finish(self):
        self.log.debug("--- CalibrationStep finish ---")
