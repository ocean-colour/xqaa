=============
The algorithm
=============

XQAA reformulates the classical Lee et al. Quasi-Analytical Algorithm (QAA).
Rather than building total absorption from an empirically anchored reference
wavelength, it inverts the reflectance model analytically at every wavelength
and exploits two spectral limits where the pure-water IOPs dominate.

The QSSA reflectance model
--------------------------

The starting point is the QSSA (Gordon) model for the sub-surface
remote-sensing reflectance,

.. math::

   r_{rs} = G_1 u + G_2 u^2, \qquad u = \frac{b_b}{a + b_b},

where :math:`a` and :math:`b_b` are the total absorption and backscattering
coefficients. The above-surface :math:`R_{rs}` is first converted to the
sub-surface :math:`r_{rs}` with the Lee+2002 relation
(:func:`xqaa.geometric.rrs_from_Rrs`):

.. math::

   r_{rs} = \frac{R_{rs}}{0.52 + 1.17\, R_{rs}} .

The quadratic inversion
-----------------------

Solving the QSSA quadratic for the physical (positive) root of :math:`u`
(:func:`xqaa.inversion.quadratic`) yields, at every wavelength, the ratio of
total absorption to total backscatter:

.. math::

   D \equiv \frac{1}{u} - 1 = \frac{a}{b_b}
     = \frac{a_w + a_{nw}}{b_{b,w} + b_{b,p}} .

Because the pure-water IOPs :math:`a_w` and :math:`b_{b,w}` are known,
:math:`D` can be inverted for the non-water IOPs directly in two spectral
limits:

* **Red limit** (:math:`\lambda > 600` nm) — water absorption dominates
  (:math:`a \approx a_w`), so (:func:`xqaa.inversion.retrieve_bbp`)

  .. math::

     b_{b,p} \approx \frac{a_w}{D} - b_{b,w} .

* **Blue limit** (oligotrophic waters, Chl :math:`< 1`) — water backscatter
  dominates (:math:`b_b \approx b_{b,w}`), so
  (:func:`xqaa.inversion.retrieve_anw`)

  .. math::

     a_{nw} \approx D \left( b_{b,w} + \langle b_{b,p} \rangle \right) - a_w ,

  where :math:`\langle b_{b,p} \rangle` is a correction built from the mean
  ``bbp`` over the red 600–650 nm window (the ``[bbmin, bbmax]`` window of
  :class:`~xqaa.params.XQAAParams`). The correction scheme is set by
  ``bbp_corr``: a :math:`\propto \lambda^{-1}` power law anchored at the
  window (``'pow'``, the default), the flat window mean (``'mean'``), or no
  correction (``'none'``).

The G coefficients
------------------

By default XQAA uses **fixed** Gordon coefficients,
:math:`G_1 = 0.0895` and :math:`G_2 = 0.1247`, at every wavelength
(``coeff_source='fixed'``). A wavelength-dependent path is available via
``coeff_source='bspline'``: B-splines fit offline
(:mod:`xqaa.qssa.derive`) to the Loisel+2023 Hydrolight dataset and shipped
as packaged ``.npz`` files (:mod:`xqaa.qssa.io`).

The reference dataset variant is Loisel+2023 with ``L23_X=1`` by default.

.. warning::

   The ``X=4`` variant of Loisel+2023 will require modelling inelastic
   processes (e.g. Raman scattering, fluorescence) before it can be used
   reliably; use ``L23_X=1`` for now.

Pure-water IOPs
---------------

The pure-water absorption :math:`a_w` comes from
`ocpy <https://github.com/ocean-colour/ocpy>`_
(``ocpy.water.absorption``). The pure-water backscatter :math:`b_{b,w}` is
currently a **stopgap**, interpolated from the selected Loisel+2023 variant;
replacing it with a proper pure-water backscatter model is future work.

.. seealso::

   :doc:`background` for the full step-by-step derivation (also maintained
   `on Overleaf <https://www.overleaf.com/read/nsspxdvmqkmv#fc6f64>`_).
