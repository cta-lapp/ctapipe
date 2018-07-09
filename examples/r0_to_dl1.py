#!/usr/bin/env python3

"""
Hillas parameters calculation of LST1 events from a simtelarray file.
Result is stored in a fits file.
Running this script for several simtelarray files will concatenate events to the same fits file.

USAGE: python LST1_Hillas.py 'Particle' 'Simtelarray file' 'Store Img(True or False)'

"""

import numpy as np
import os
from ctapipe.image import hillas_parameters, tailcuts_clean
from ctapipe.io import event_source
from ctapipe.calib import CameraCalibrator
import argparse
from ctapipe.utils import get_dataset
from ctapipe.io import HDF5TableWriter
from ctapipe.reco import HillasReconstructor

import astropy.units as u

parser = argparse.ArgumentParser(description="process CTA files.")

# Required argument
parser.add_argument('--filename', '-f', type=str,
                    dest='filename',
                    help='path to the file to process',
                    default=get_dataset('gamma_test.simtel.gz'))

# Optional arguments
parser.add_argument('--ptype', '-t', dest='particle_type', action='store',
                    default=None,
                    help='Particle type (gamma, proton, electron) - subfolders where simtelarray files of different type are stored)'
                         'Optional, if not passed, the type will be guessed from the filename'
                         'If not guessed, "unknown" type will be set'
                    )

parser.add_argument('--outdir', '-o', dest='outdir', action='store',
                    default='./results/',
                    help='Output directory to save fits file.'
                    )
parser.add_argument('--filetype', '-ft', dest='filetype', action='store',
                    default='hdf5', type=str,
                    help='String. Type of output file: hdf5 or fits'
                         'Default=hdf5'
                    )
parser.add_argument('--storeimg', '-s', dest='storeimg', action='store',
                    default=False, type=bool,
                    help='Boolean. True for storing pixel information.'
                         'Default=False, any user input will be considered True'
                    )

args = parser.parse_args()


def guess_type(filename):
    """
    Guess the particle type from the filename

    Parameters
    ----------
    filename: str

    Returns
    -------
    str: 'gamma', 'proton', 'electron' or 'unknown'
    """
    particles = ['gamma', 'proton', 'electron']
    for p in particles:
        if p in filename:
            return p
    return 'unknown'


class HillasNotFinite(Exception):
    """
    Error to be raised when hillas parameters are not finite
    """
    pass


if __name__ == '__main__':

    # Some configuration variables
    ########################################################
    filename = args.filename
    particle_type = guess_type(filename) if args.particle_type is None else args.particle_type

    storeimg = args.storeimg

    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)

    filetype = args.filetype
    outfile = args.outdir + '/' + particle_type + "_events." + filetype  # File where DL2 data will be stored



    #######################################################

    # Setup the calibration to use:
    cal = CameraCalibrator(None, None, r1_product='HESSIOR1Calibrator', \
                           extractor_product='NeighbourPeakIntegrator')

    # Cleaning levels:
    picture_threshold = 6
    boundary_threshold = 0

    source = event_source(filename)     # Open the file
    source.allowed_tels = {1, 2, 3, 4}
    source.max_events = 10  # Limit the number of events to load - useful for tests

    hillas_reco = HillasReconstructor()

    with HDF5TableWriter(filename=outfile, group_name='dl1', overwrite=True) as writer:

        for i, event in enumerate(source):
            if i % 100 == 0:
                print("EVENT_ID: ", event.r0.event_id, "TELS: ",
                      event.r0.tels_with_data,
                      "MC Energy:", event.mc.energy)

            ntels = len(event.r0.tels_with_data)

            cal.calibrate(event)

            hillas_dict = {}
            pointing_azimuth = {}
            pointing_altitude = {}

            for ii, tel_id in enumerate(event.r0.tels_with_data):

                camera = event.inst.subarray.tel[tel_id].camera

                chan = 0
                signals = event.dl1.tel[tel_id].image[chan]

                # Apply image cleaning
                cleanmask = tailcuts_clean(camera, signals,
                                           picture_thresh=picture_threshold,
                                           boundary_thresh=boundary_threshold,
                                           keep_isolated_pixels=False,
                                           min_number_picture_neighbors=1,
                                           )

                image = event.dl1.tel[tel_id].image[chan]

                if np.max(image[cleanmask]) < 1.e-6:  # skip images with no pixels
                    continue

                try:
                    hillas = hillas_parameters(camera[cleanmask], image[cleanmask])

                    if not all(map(np.isfinite, hillas.values())):
                        raise HillasNotFinite("bad Hillas parameters")

                    hillas_dict[tel_id] = hillas
                    pointing_azimuth[tel_id] = event.mc.tel[tel_id].azimuth_raw * u.rad
                    pointing_altitude[tel_id] = event.mc.tel[tel_id].altitude_raw * u.rad
                    # pointing_altitude[tel_id] = ((np.pi / 2) - event.mc.tel[
                    # tel_id].altitude_raw) * u.rad  # this is weird to say the least.

                    writer.write("hillas", hillas)

                except HillasNotFinite:
                    pass



                if len(hillas_dict) < 2:
                    print("mono")
                    # raise TooFewTelescopesException()
                else:
                    reconstruction = hillas_reco.predict(hillas_dict, event.inst, pointing_azimuth, pointing_altitude)
                    writer.write("reconstruction", reconstruction)


                # writer.write("hillas", hillas)
                writer.write("mc", event.mc)

    # writer.write("camera", event.inst.subarray.tel[tel_id])
