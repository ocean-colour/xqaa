""" Tests for the inversion module (no external deps beyond packaged data). """
import numpy as np

import pytest

from xqaa import inversion
from xqaa import params as xqaa_params


def test_quadratic_roundtrip():
    """ quadratic() should recover D = 1/u - 1 from a synthesized rrs. """
    G1 = np.array([0.0895, 0.0895])
    G2 = np.array([0.1247, 0.1247])
    u_true = np.array([0.3, 0.5])

    # Forward QSSA model, then invert
    rrs = G1*u_true + G2*u_true**2
    D = inversion.quadratic(rrs, G1, G2)

    assert np.allclose(D, 1.0/u_true - 1.0)


def test_quadratic_negative_raises():
    """ A negative (unphysical) u should raise. """
    G1 = np.array([0.0895])
    G2 = np.array([0.1247])
    rrs = np.array([-0.01])  # drives u negative

    with pytest.raises(ValueError):
        inversion.quadratic(rrs, G1, G2)


def test_retrieve_bbp_and_anw():
    """ Red-limit bbp and blue-limit anw are simple algebra of aw, bbw, D. """
    aw = np.array([0.5, 0.4])
    bbw = np.array([0.01, 0.02])
    D = np.array([2.0, 4.0])

    # bbp = aw/D - bbw
    bbp = inversion.retrieve_bbp(aw, bbw, D)
    assert np.allclose(bbp, aw/D - bbw)

    # anw = D*bbw - aw  (no correction)
    anw = inversion.retrieve_anw(aw, bbw, D)
    assert np.allclose(anw, D*bbw - aw)

    # With a correction, anw gains D*corr_bbp
    corr = 0.001
    anw_c = inversion.retrieve_anw(aw, bbw, D, corr_bbp=corr)
    assert np.allclose(anw_c, D*bbw - aw + corr*D)


def test_calc_Gcoeff_shapes():
    """ calc_Gcoeff evaluates the packaged B-splines (no ocpy needed). """
    xparams = xqaa_params.XQAAParams()
    wave = np.linspace(450., 650., 20)

    G1, G2 = inversion.calc_Gcoeff(wave, xparams)
    assert G1.shape == wave.shape
    assert G2.shape == wave.shape
    assert np.all(np.isfinite(G1)) and np.all(np.isfinite(G2))
