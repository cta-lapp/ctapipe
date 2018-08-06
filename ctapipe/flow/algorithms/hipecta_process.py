from ctapipe.core import Component
from ctapipe.image import TelescopeReco



class HiPeCTAProcess(Component):


    def init(self):
        self.log.debug("--- HiPeCTAProcess init ---")
        self.reco = TelescopeReco(wavelet_threshold=3, hillas_threshold_signal_tel=500)
        return True

    def run(self, event):
        for tel_id in list(event.r0.tels_with_data):
            tabHillas, reco_status = self.reco.process(tel_id, event)
            yield tabHillas, reco_status

    def finish(self):
        self.log.debug("--- HiPeCTAProcess finish ---")
