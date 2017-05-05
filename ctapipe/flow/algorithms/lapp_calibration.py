from ctapipe.core import Component
from traitlets import Unicode
from subprocess import Popen
from ctapipe.flow.algorithms.in_out_process import InOutProcess



class LappCalibration(InOutProcess):

    exe = Unicode(help='executable').tag(
        config=True, allow_none=False)

    """CalibrationStep` class represents a Stage for pipeline.
        it executes prun2pcalibrun
    """
