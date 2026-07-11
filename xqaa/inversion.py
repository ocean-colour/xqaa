""" Algorithms related to the QSSA inversion.

The XQAA inversion rests on the QSSA (Gordon) reflectance model

    rrs = G1*u + G2*u**2 ,   with   u = bb / (a + bb)

Solving that quadratic for the physical (positive) root of ``u`` yields, at
each wavelength, the ratio of total absorption to total backscatter

    D = 1/u - 1 = a / bb = (aw + anw) / (bbw + bbp) .

Because the pure-water IOPs ``aw`` and ``bbw`` are known, ``D`` is then used to
solve for the non-water absorption (anw) in the blue and the particulate
backscatter (bbp) in the red.
"""
import numpy as np

from xqaa.qssa.io import load_qssa_bspline
from xqaa import params as xqaa_params


def calc_Gcoeff(wave: np.ndarray, xparams: xqaa_params.XQAAParams):
    """
    Evaluate the QSSA G1 and G2 coefficients at the requested wavelengths.

    By default (``xparams.coeff_source == 'fixed'``) the fixed Gordon
    constants ``xparams.G1``/``xparams.G2`` are used at every wavelength.
    Setting ``coeff_source == 'bspline'`` instead evaluates the
    wavelength-dependent B-splines fit offline from the reference dataset
    (see ``xqaa.qssa.derive``).

    Parameters:
        wave (np.ndarray): Wavelengths at which to evaluate the coefficients [nm].
        xparams (XQAAParams): The parameters for the XQAA model; selects the
            coefficient source and, for B-splines, the dataset / variant.

    Returns:
        tuple: ``(G1, G2)`` arrays, each with the same shape as ``wave``.
    """
    if xparams.coeff_source == 'fixed':
        # Fixed Gordon coefficients, broadcast across all wavelengths
        G1 = np.full(np.shape(wave), xparams.G1, dtype=float)
        G2 = np.full(np.shape(wave), xparams.G2, dtype=float)
    elif xparams.coeff_source == 'bspline':
        # Wavelength-dependent coefficients from the pre-fit B-splines
        bspline_G1, bspline_G2 = load_qssa_bspline(xparams)
        G1 = bspline_G1(wave)
        G2 = bspline_G2(wave)
    else:
        raise ValueError(f"Bad coeff_source: {xparams.coeff_source}")

    return G1, G2


def quadratic(rrs: np.ndarray,
              G1: np.ndarray, G2: np.ndarray):
    """
    Invert the QSSA quadratic ``rrs = G1*u + G2*u**2`` for ``D = a/bb``.

    Writing the quadratic as ``G2*u**2 + G1*u - rrs = 0`` and keeping the
    positive root::

        u = (-G1 + sqrt(G1**2 + 4*G2*rrs)) / (2*G2)
        D = 1/u - 1

    Parameters:
        rrs (np.ndarray): Sub-surface remote-sensing reflectance [1/sr].
        G1 (np.ndarray): QSSA linear coefficient (per wavelength).
        G2 (np.ndarray): QSSA quadratic coefficient (per wavelength).

    Returns:
        np.ndarray: ``D = a/bb``, the ratio of total absorption to total
            backscatter, with the same shape as ``rrs``.

    Raises:
        ValueError: If any element of the recovered ``u`` is negative
            (unphysical), which would otherwise yield a spurious ``D``.
    """
    # Positive root of the QSSA quadratic -> u = bb/(a+bb)
    sq = np.sqrt(G1**2 + 4*G2*rrs)
    upos = (-1*G1 + sq)/(2*G2)

    # u must be physical (positive); flag if not
    bad = upos < 0
    if np.any(bad):
        raise ValueError("Negative values of u in the quadratic inversion")

    # D = 1/u - 1 = a/bb
    D = 1/upos - 1

    return D


def retrieve_anw(aw: np.ndarray, bbw: np.ndarray, D: np.ndarray,
                 corr_bbp: float = None):
    """
    Retrieve the non-water absorption coefficient (anw) in the blue limit.

    In the blue, pure-water backscatter dominates so ``bb ~ bbw`` and, from
    ``D = (aw + anw)/(bbw + bbp)``, ``anw ~ D*bbw - aw``. A backscatter
    correction ``+ D*corr_bbp`` optionally accounts for the (small but
    non-negligible) particulate backscatter.

    Parameters:
        aw (np.ndarray): Pure-water absorption coefficient [1/m].
        bbw (np.ndarray): Pure-water backscattering coefficient [1/m].
        D (np.ndarray): The a/bb ratio from :func:`quadratic`.
        corr_bbp (np.ndarray or float, optional): Correction term for the
            particulate backscatter; if given, ``D*corr_bbp`` is added.

    Returns:
        np.ndarray: Non-water absorption coefficient anw [1/m].
    """
    # Blue-limit inversion: anw ~ D*bbw - aw
    anw = D*bbw - aw

    # Optionally fold in the particulate-backscatter correction
    if corr_bbp is not None:
        anw += corr_bbp*D

    return anw


def retrieve_bbp(aw: np.ndarray, bbw: np.ndarray, D: np.ndarray):
    """
    Retrieve the particulate backscattering coefficient (bbp) in the red limit.

    In the red, pure-water absorption dominates so ``a ~ aw`` and, from
    ``D = (aw + anw)/(bbw + bbp)``, ``bbp ~ aw/D - bbw``.

    Parameters:
        aw (np.ndarray): Pure-water absorption coefficient [1/m].
        bbw (np.ndarray): Pure-water backscattering coefficient [1/m].
        D (np.ndarray): The a/bb ratio from :func:`quadratic`.

    Returns:
        np.ndarray: Particulate (non-water) backscattering coefficient bbp [1/m].
    """
    # Red-limit inversion: bbp ~ aw/D - bbw
    bbp = aw/D - bbw

    return bbp
