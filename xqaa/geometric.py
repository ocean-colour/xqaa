""" Geometric considerations for converting reflectances. """

import numpy as np


def rrs_from_Rrs(Rrs: np.ndarray):
    """
    Convert above-surface remote-sensing reflectance (Rrs) to the
    sub-surface remote-sensing reflectance (rrs) using the Lee+2002
    relation ``rrs = Rrs / (A + B*Rrs)``.

    Parameters:
        Rrs (np.ndarray): Above-surface remote-sensing reflectance [1/sr].

    Returns:
        np.ndarray: Sub-surface remote-sensing reflectance rrs [1/sr],
            with the same shape as ``Rrs``.
    """
    # Lee+2002 coefficients for the Rrs -> rrs conversion
    A, B = 0.52, 1.17

    # Apply the conversion element-wise
    rrs = Rrs / (A + B * Rrs)

    return rrs
