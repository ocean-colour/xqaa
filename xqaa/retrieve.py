""" Methods for the XQAA retrieval """
import warnings

import numpy as np

from ocpy.water import absorption
from ocpy.hydrolight import loisel23

from xqaa.params import XQAAParams
from xqaa import geometric as xqaa_geom
from xqaa import inversion


def iops_from_Rrs(wave: np.ndarray, Rrs: np.ndarray,
                  xparams: XQAAParams):
    """
    Retrieve the inherent optical properties (IOPs) from remote-sensing
    reflectance using the XQAA inversion.

    The steps are: convert Rrs -> rrs, evaluate the QSSA G-coefficients,
    invert the quadratic for ``D = a/bb``, solve the red limit for the
    particulate backscatter ``bbp``, build a backscatter correction, and
    solve the blue limit for the non-water absorption ``anw``.

    Parameters:
        wave (np.ndarray): Wavelengths [nm].
        Rrs (np.ndarray): Above-surface remote-sensing reflectance [1/sr],
            same shape as ``wave``.
        xparams (XQAAParams): XQAA parameters (dataset/variant, bbp window,
            and correction scheme).

    Returns:
        dict: The retrieval, with keys
            ``anw`` (np.ndarray, non-water absorption [1/m]),
            ``bbp`` (np.ndarray, particulate backscatter [1/m]),
            ``corr_bbp`` (np.ndarray or float, the applied bbp correction), and
            ``avg_bbp`` (float, mean bbp over the [bbmin, bbmax] window).
    """

    # Pure-water absorption from ocpy
    aw = absorption.a_water(wave)

    # Pure-water backscatter: stopgap that reads bbw from the selected
    # Loisel+2023 variant (honors xparams) until a proper b_w model lands.
    warnings.warn("Need to implement b_w")
    l23_ds = loisel23.load_ds(xparams.L23_X, xparams.L23_Y)
    l23_bbw = (l23_ds.bb.data - l23_ds.bbnw.data)[0]
    bbw = np.interp(wave, l23_ds.Lambda.data, l23_bbw)

    # Sub-surface reflectance
    rrs = xqaa_geom.rrs_from_Rrs(Rrs)

    # QSSA coefficients and the a/bb ratio D
    G1, G2 = inversion.calc_Gcoeff(wave, xparams)
    D = inversion.quadratic(rrs, G1, G2)

    # Red-limit particulate backscatter
    bbp = inversion.retrieve_bbp(aw, bbw, D)

    # Wavelengths used to average bbp for the correction
    avgbb_wvs = (wave > xparams.bbmin) & (wave < xparams.bbmax)
    avg_bbp = np.nanmean(bbp[avgbb_wvs])

    # Build the backscatter correction used in the blue-limit anw solve
    if xparams.bbp_corr == 'mean':
        # Flat correction: the window mean at every wavelength
        corr_bbp = avg_bbp
    elif xparams.bbp_corr == 'pow':
        # Power-law (~1/wave) correction anchored at the window
        corr_bbp = avg_bbp*(wave/np.mean(wave[avgbb_wvs]))**(-1)
    elif xparams.bbp_corr == 'none':
        # No correction
        corr_bbp = 0.
    else:
        raise ValueError(f"Bad bbp_corr: {xparams.bbp_corr}")

    # Blue-limit non-water absorption
    anw = inversion.retrieve_anw(aw, bbw, D, corr_bbp=corr_bbp)

    return {'anw': anw, 'bbp': bbp, 'corr_bbp': corr_bbp, 'avg_bbp': avg_bbp}
