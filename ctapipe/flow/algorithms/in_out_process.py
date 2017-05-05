from ctapipe.core import Component
from traitlets import Unicode
from subprocess import Popen
from ctapipe.flow.algorithms.build_command import build_command



class InOutProcess(Component):
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
            cmd, _ = build_command(self.exe,  in_filename, )
            self.log.info("--- InOutProcess cmd {} --- in_filename {}".format(cmd, in_filename))
            proc = Popen(cmd)
            proc.wait()
            self.log.debug("--- CalibrationStep STOP ---")
            return ("file {} Done".format(in_filename))

    def finish(self):
        self.log.debug("--- CalibrationStep finish ---")
        pass
