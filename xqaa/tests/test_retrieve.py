""" Tests for the retrieve module. """
import os

import numpy as np
import pandas

import pytest

# The end-to-end retrieval needs ocpy (aw + Loisel23 bbw); skip if absent.
pytest.importorskip("ocpy")

from xqaa import params as xqaa_params
from xqaa import retrieve

# Resolve the test data relative to this file (not the cwd)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')


def test_iop_from_Rrs():
    """ End-to-end check of iops_from_Rrs against golden values. """
    xqaaParams = xqaa_params.XQAAParams()

    # Load the reference Rrs spectrum
    df = pandas.read_csv(os.path.join(DATA_DIR, 'test_Rrs.csv'))

    # Run the retrieval
    result = retrieve.iops_from_Rrs(
        df.wave.values, df.Rrs.values, xqaaParams)

    # Golden values regenerated 2026-07-02 with the X=4 default (ocean14/ocpy)
    assert np.isclose(result.anw[-1], 0.08494522800146487, atol=1e-5)
    assert np.isclose(result.bbp[-1], 0.00046071271876868373, atol=1e-5)
    assert np.isclose(result.avg_bbp, 0.0005777785114588882, atol=1e-8)
