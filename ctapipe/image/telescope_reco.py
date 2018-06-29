import numpy as np
import ctapipe
import hipecta.core
import astropy.units as u
from ctapipe.io.containers import HillasParametersContainer
from astropy.coordinates import Angle
from ctapipe.core import Component





'''
TO:
-1 Set a config by telescope_type
updateRecoTemporaryWithRefShape and createRecoTemporary
create a temporaire without gain and pedestal
'''

class Telescope_info():
    def __init__(self, reco_temporary):
        """
        Attributes
        ----------
        reco_temporary: hipecta.core.PRecoTemporary
        Parameters
        ----------
        reco_temporary: hipecta.core.PRecoTemporary containing:
            focalLength, matNeighbourQuadSum, nbSliceBeforPeak, matCalibratedSignal,
            matNeighbourSlice, nbSliceWindow, matKeepSignalQuad, matSignal,
            newMatCalibratedSignal, matNeighbourPixelSum, matSignalQuad,
            newMatKeepSignalQuad
        """

        self.reco_temporary = reco_temporary


class TelescopeReco(Component):
    """
    Process a raw telescope waveform (R1) to DL1 (Hillas parameters)
    """

    def __init__(self, config=None, tool=None,
                    waveletThreshold=3,
                    hillasThresholdSignalTel=500,
                     **kwargs):
        """
        handle the r0 to dl1 reconstruction. Calibration/Integration/Cleaning/Hillas.

        Attributes
        ----------
        telescope_info : dictionary
            Python dict. key is telescope id. Value is an instance of Telscope_info
        Parameters
        ----------
        config : traitlets.loader.Config
            Configuration specified by config file or cmdline arguments.
            Used to set traitlet values.
            Set to None if no configuration to pass.
        tool : ctapipe.core.Tool or None
            Tool executable that is calling this component.
            Passes the correct logger to the component.
            Set to None if no Tool to pass.
        waveletThreshold : int
            Wavelet cleaning threshold.
        hillasThresholdSignalTel: int
            The hillas threshold
        kwargs
        """
        super().__init__(config=config, parent=tool, **kwargs)

        self.telescope_info = dict()
        self.cut_config = hipecta.core.PConfigCut()
        self.cut_config.waveletThreshold = waveletThreshold
        self.cut_config.hillasThresholdSignalTel = hillasThresholdSignalTel


    def add_telescope(self, telescope_id, number_samples,
                      telescope_description: ctapipe.instrument.TelescopeDescription,
                      camera: ctapipe.io.containers.MCCameraEventContainer):
        """
        Add a telescope information and create gain and pedestal arrays

        Parameters
        ----------
        telescope_id: int
        TelescopeDescription: `ctapipe.instrument.telescope.TelescopeDescription`
        pixels_position : numpy ndarray
            telescope's pixels position: (x,y) of shape (number of pixels, 2)

        Returns
        -------
        """



        pixels_position = np.ascontiguousarray(np.transpose([telescope_description.camera.pix_x.to(u.m).value,
                                                             telescope_description.camera.pix_y.to(
                                                                           u.m).value]).astype(np.float32))

        gain_high = camera.dc_to_pe[0]
        try:
            gain_low = camera.dc_to_pe[1]
        except:
            gain_low = camera.dc_to_pe[0]

        pedestal_high = camera.pedestal[0]
        try:
            pedestal_low = camera.pedestal[1]
        except:
            pedestal_low = camera.pedestal[0]

        reference_shape = camera.reference_pulse_shape[0].astype(np.float32)


        reco_temporary = hipecta.core.createRecoTemporary(number_samples,
                                         0,
                                         pixels_position,
                                         gain_high,
                                         gain_low,
                                         pedestal_high,
                                         pedestal_low,
                                         )

        hipecta.core.updateRecoTemporaryWithRefShape(reco_temporary, reference_shape, 0.1)

        self.telescope_info[telescope_id] = Telescope_info(reco_temporary)



    def getHillasParametersContainer(self, hillas_param):
        """
        convert tuple of hillas parameter (from HiPeCTA to ctapipe HillasParametersContainer

        Parameters
        ----------
        hillas_param: tuples containaing hillas paramters
        Returns
        -------
        ctapipe HillasParametersContainer
        """
        return HillasParametersContainer(intensity=hillas_param[hipecta.core.getHillasImageAmplitude()],
                                        x=hillas_param[hipecta.core.getHillasGx()] * u.m,
                                        y=hillas_param[hipecta.core.getHillasGy()] * u.m,
                                        width=np.sqrt(2) * hillas_param[hipecta.core.getHillasLength()] * u.m,
                                        length=np.sqrt(2) * hillas_param[hipecta.core.getHillasWidth()] * u.m,
                                        r=np.sqrt(hillas_param[hipecta.core.getHillasGx()] ** 2
                                                  + hillas_param[hipecta.core.getHillasGy()] ** 2) * u.m,
                                        phi=Angle(hillas_param[hipecta.core.getHillasPhi()] * u.rad),
                                        psi=Angle(
                                        (hillas_param[hipecta.core.getHillasDirection()] + np.pi / 2) * u.rad),
                                            # miss = 0,
                                        skewness=hillas_param[hipecta.core.getHillassSewness()],
                                        kurtosis=hillas_param[hipecta.core.getHillasKurtosis()]
                                        )


    def _process(self, telescope_id, waveform):
        """
        Process a waveform and return its Hillas parameters

        Parameters
        ----------
        waveform: `numpy.ndarray` of shape (number_slice,

        Returns
        -------
        Hillas parameters
        """
        reco_temporary = self.telescope_info[telescope_id].reco_temporary
        hillas_parameters, event_reco = hipecta.core.fullAnalysis(waveform, self.cut_config, reco_temporary)

        return hillas_parameters, event_reco




    def process(self, telescope_id, event):
        """
        Process a ctapipe r0 event and return its Hillas parameters

        Parameters
        ----------
        event: ctapipe.io.containers.DataContainer
        Returns
        -------
        Hillas parameters
        """
        if not telescope_id in self.telescope_info:
            self.add_telescope(telescope_id, event.r0.tel[telescope_id].num_samples,
                               event.inst.subarray.tel[telescope_id],
                               event.mc.tel[telescope_id])

        waveform = event.r0.tel[telescope_id].waveform
        matslice = np.ascontiguousarray(waveform[0].T)
        return self._process(telescope_id, matslice)
