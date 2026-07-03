""" Tests for the params module. """
from xqaa import params as xqaa_params


def test_default_params():
    """ Check the XQAAParams defaults. """
    xqaaParams = xqaa_params.XQAAParams()

    assert xqaaParams.dataset == 'loisel23'
    assert xqaaParams.L23_X == 1
    assert xqaaParams.L23_Y == 0
    assert xqaaParams.bbp_corr == 'pow'
    # Fixed Gordon coefficients are the default coefficient source
    assert xqaaParams.coeff_source == 'fixed'
    assert xqaaParams.G1 == 0.0895
    assert xqaaParams.G2 == 0.1247


def test_chk_options():
    """ chk_options validates a field value against its metadata options. """
    xqaaParams = xqaa_params.XQAAParams()

    # Default 'pow' is a valid option
    assert xqaaParams.chk_options('bbp_corr')

    # An invalid value is rejected
    xqaaParams.bbp_corr = 'not-an-option'
    assert not xqaaParams.chk_options('bbp_corr')
