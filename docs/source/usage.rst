==========
Quickstart
==========

The top-level entry point is :func:`xqaa.retrieve.iops_from_Rrs`: hand it a
wavelength grid, an above-surface remote-sensing reflectance spectrum, and an
:class:`~xqaa.params.XQAAParams` configuration, and it returns the retrieved
IOPs as a dict.

Basic retrieval
---------------

.. code-block:: python

   import numpy as np
   from xqaa import params, retrieve

   # wave [nm] and Rrs [1/sr] are your input spectrum, e.g.
   # wave = np.arange(400., 701., 5.)
   # Rrs  = ...  (same shape as wave)

   # Default configuration: fixed Gordon coefficients, power-law bbp correction
   xparams = params.XQAAParams()

   # Run the retrieval
   result = retrieve.iops_from_Rrs(wave, Rrs, xparams)

The returned dict has four keys:

* ``result['anw']`` — non-water absorption coefficient :math:`a_{nw}` [1/m]
  (numpy array, valid in the blue).
* ``result['bbp']`` — particulate backscattering coefficient :math:`b_{b,p}`
  [1/m] (numpy array, valid in the red).
* ``result['corr_bbp']`` — the applied backscatter correction (array for
  ``bbp_corr='pow'``, scalar otherwise).
* ``result['avg_bbp']`` — mean ``bbp`` over the ``[bbmin, bbmax]`` window
  (float).

Plotting the result
-------------------

.. code-block:: python

   import matplotlib.pyplot as plt

   fig, axes = plt.subplots(1, 2, figsize=(10, 4))

   axes[0].plot(wave, result['anw'])
   axes[0].set_xlabel('Wavelength (nm)')
   axes[0].set_ylabel(r'$a_{nw}$ (1/m)')

   axes[1].plot(wave, result['bbp'])
   axes[1].set_xlabel('Wavelength (nm)')
   axes[1].set_ylabel(r'$b_{b,p}$ (1/m)')

   plt.tight_layout()
   plt.show()

A worked end-to-end example lives in the repository notebook
``nb/XQAA_demo.ipynb``.

Key configuration knobs
-----------------------

:class:`~xqaa.params.XQAAParams` is a dataclass; override any field at
construction:

.. code-block:: python

   xparams = params.XQAAParams(coeff_source='bspline', bbp_corr='mean')

* ``coeff_source`` — source of the QSSA :math:`G_1`/:math:`G_2` coefficients.
  ``'fixed'`` (default) uses the Gordon constants ``G1=0.0895``,
  ``G2=0.1247`` at every wavelength; ``'bspline'`` evaluates the
  wavelength-dependent B-splines fit offline to Loisel+2023 (see
  :doc:`algorithm`).
* ``bbp_corr`` — the backscatter correction used in the blue-limit ``anw``
  solve: ``'pow'`` (default; a :math:`\propto \lambda^{-1}` power law
  anchored at the averaging window), ``'mean'`` (the flat window mean), or
  ``'none'``.
* ``bbmin``, ``bbmax`` — the red window (default 600–650 nm) over which
  ``bbp`` is averaged for the correction.
* ``dataset``, ``L23_X``, ``L23_Y`` — the reference dataset variant
  (currently Loisel+2023, default ``L23_X=1``, ``L23_Y=0``) used for the
  B-spline coefficients and the stopgap pure-water backscatter.

.. warning::

   The Loisel+2023 ``X=4`` variant will require modelling inelastic
   processes (e.g. Raman scattering, fluorescence); use ``L23_X=1`` for now.
