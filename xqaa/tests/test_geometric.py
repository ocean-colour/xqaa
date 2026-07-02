""" Tests for the geometric module (no external deps). """
import numpy as np

from xqaa import geometric


def test_rrs_from_Rrs():
    """ rrs = Rrs / (0.52 + 1.17*Rrs), element-wise. """
    Rrs = np.array([0.0, 0.01, 0.05])
    rrs = geometric.rrs_from_Rrs(Rrs)

    expected = Rrs / (0.52 + 1.17*Rrs)
    assert np.allclose(rrs, expected)

    # Zero maps to zero; output preserves shape
    assert rrs[0] == 0.0
    assert rrs.shape == Rrs.shape
