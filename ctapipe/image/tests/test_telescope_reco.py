from ctapipe.io import event_source
from ctapipe.utils import get_dataset
from ctapipe.image import TelescopeReco
import numpy as np


def test_hillas():
    filename=get_dataset("gamma_test_large.simtel.gz")
    reco = TelescopeReco(waveletThreshold=3, hillasThresholdSignalTel=500)
    with event_source(filename) as source:
        for event in source:
            for tel_id in list(event.dl0.tels_with_data):
                tabHillas, reco_status = reco.process(tel_id, event)
                ctapipe_hillas = reco.getHillasParametersContainer(tabHillas)
                assert np.isclose(ctapipe_hillas.intensity, 220.92934)
                assert np.isclose(ctapipe_hillas.kurtosis, -2.9893093)
                assert np.isclose(ctapipe_hillas.length.value, 0.03703341)
                assert np.isclose(ctapipe_hillas.phi.value, 1.5518157)
                assert np.isclose(ctapipe_hillas.psi.value, 4.17142446)
                assert np.isclose(ctapipe_hillas.r.value, 1.14662413)
                assert np.isclose(ctapipe_hillas.skewness, -0.019652579)
                assert np.isclose(ctapipe_hillas.width.value, 0.0720041)
                assert np.isclose(ctapipe_hillas.x.value, - 0.6133044)
                assert np.isclose(ctapipe_hillas.y.value, - 0.9688161)
                break;
            break;
