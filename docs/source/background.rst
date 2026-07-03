==================================
Algorithm background (derivation)
==================================

This page folds the author's LaTeX writeup of the XQAA derivation into the
documentation. It uses the package's variable names (``anw``, ``bbp``); the
paper's original notation writes the non-water backscatter as
:math:`b_{b,nw}`, which for XQAA is the particulate backscatter
:math:`b_{b,p}`.

.. note::

   The full, living derivation is maintained on Overleaf:
   `https://www.overleaf.com/read/nsspxdvmqkmv#fc6f64
   <https://www.overleaf.com/read/nsspxdvmqkmv#fc6f64>`_.

The QSSA reflectance model
--------------------------

As first derived by James Hansen (1971) and then adopted by Gordon (1973),
the sub-surface remote-sensing reflectance is well approximated by the
quasi single scattering approximation (QSSA):

.. math::
   :label: qssa

   r_{rs}(\lambda) = G_1\, u(\lambda) + G_2\, u(\lambda)^2 ,

with

.. math::
   :label: def-u

   u(\lambda) \equiv \frac{b_b(\lambda)}{a(\lambda) + b_b(\lambda)} ,

where :math:`a(\lambda)` and :math:`b_b(\lambda)` are the total absorption
and backscattering coefficients. Comparison against full radiative-transfer
calculations (the Hydrolight outputs of Loisel et al. 2023, hereafter L23)
shows the QSSA is a good description of :math:`r_{rs}` versus :math:`u`.

The community, following Gordon, has generally assumed that the coefficients
:math:`G_1, G_2` in :eq:`qssa` are independent of wavelength. The L23
calculations show this is not strictly the case, but XQAA adopts the same
assumption by default; the formalism that follows accommodates
:math:`G_1(\lambda), G_2(\lambda)` without modification (and XQAA offers a
wavelength-dependent B-spline path, ``coeff_source='bspline'``).

The above-surface remote-sensing reflectance :math:`R_{rs}` is related to
the sub-surface :math:`r_{rs}` by the standard (Lee et al. 2002) conversion:

.. math::
   :label: rrs-from-Rrs

   r_{rs}(\lambda) = \frac{R_{rs}(\lambda)}{0.52 + 1.17\, R_{rs}(\lambda)} .

Clearly, if :math:`r_{rs}` is held constant, then so too is :math:`R_{rs}`.

Solving the quadratic
---------------------

Equation :eq:`qssa` is a standard quadratic in :math:`u`. Taking the
physical (positive) root,

.. math::
   :label: u-root

   u = \frac{-G_1 + \sqrt{G_1^2 + 4 G_2\, r_{rs}}}{2 G_2} ,

where :math:`u`, :math:`r_{rs}`, :math:`G_1`, and :math:`G_2` may all be
functions of :math:`\lambda`. Call the right-hand side of :eq:`u-root` a
number :math:`C(\lambda)`. Then, with the definition of :math:`u`
(:eq:`def-u`), a little algebra recovers the ratio of total absorption to
total backscatter:

.. math::
   :label: a-over-bb

   \frac{a(\lambda)}{b_b(\lambda)} = \frac{1}{C(\lambda)} - 1 .

Defining :math:`D(\lambda) \equiv 1/C(\lambda) - 1` and separating the water
and non-water contributions yields the XQAA approximation:

.. math::
   :label: xiop

   D(\lambda) = \frac{a}{b_b}
              = \frac{a_w(\lambda) + a_{nw}(\lambda)}
                     {b_{b,w}(\lambda) + b_{b,p}(\lambda)} .

Because the pure-water IOPs :math:`a_w` and :math:`b_{b,w}` are known,
:eq:`xiop` can be inverted for the non-water IOPs in two spectral limits.

Red wavelengths: the ``bbp`` retrieval
--------------------------------------

At long wavelengths, :math:`\lambda > 600` nm, water absorption dominates,
i.e. :math:`a_w \gg a_{nw}`. In this limit, rearranging :eq:`xiop` solves
for the particulate backscattering coefficient:

.. math::
   :label: bbp-red

   b_{b,p}(\lambda) \approx \frac{a_w(\lambda)}{D(\lambda)}
                            - b_{b,w}(\lambda) .

To the extent that :math:`b_{b,w}` is known accurately at these wavelengths
(it is), this is a direct estimate of ``bbp``.

Blue wavelengths: the ``anw`` retrieval
---------------------------------------

In most oligotrophic ocean waters (Chl :math:`a < 1`), backscattering at
blue wavelengths is dominated by pure water: :math:`b_{b,w} \gg b_{b,p}`.
This allows an estimate of the non-water absorption coefficient:

.. math::
   :label: anw-blue

   a_{nw}(\lambda) \approx D(\lambda)\, b_{b,w}(\lambda) - a_w(\lambda) .

In practice, the contribution of :math:`b_{b,p}` is non-negligible even in
the blue. XQAA therefore folds in an estimate of its value from the red
retrieval :eq:`bbp-red`:

.. math::
   :label: anw-corr

   a_{nw}(\lambda) \approx D(\lambda)
       \left[\, b_{b,w}(\lambda) + \langle b_{b,p} \rangle \,\right]
       - a_w(\lambda) ,

where :math:`\langle b_{b,p} \rangle` is the mean of :math:`b_{b,p}` over
600–650 nm. (The implementation exposes the window and the correction
scheme — power law, flat mean, or none — through
:class:`~xqaa.params.XQAAParams`; see :doc:`algorithm`.)

Error propagation
-----------------

Error propagation for XQAA follows standard practice, e.g. for the
absorption,

.. math::

   \sigma^2(a) = \left| \frac{\partial a}{\partial r_{rs}} \right|^2
                 \sigma^2(r_{rs}) ,

although the algebra is somewhat involved.

Sensitivity of ``bbp`` to :math:`G_1`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Empirically, the retrieved :math:`b_{b,p}` is sensitive to error in
:math:`G_1`. Propagating an uncertainty :math:`\sigma(G_1)` through the
inversion,

.. math::

   \sigma^2(b_{b,p}) =
     \left| \frac{\partial b_{b,p}}{\partial G_1} \right|^2 \sigma^2(G_1)
   =
     \left[ \frac{a_w + a_{nw}}{(1 - u(\lambda))^2} \right]
     \left[ \frac{-1 + \dfrac{G_1}{\sqrt{G_1^2 + 4 G_2\, r_{rs}}}}
                 {2 G_2} \right]^2
     \sigma^2(G_1) ,

which quantifies why the red-limit ``bbp`` inherits a comparatively large
error from :math:`G_1`.
