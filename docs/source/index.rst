.. XQAA documentation master file

====================================================
XQAA: an improved Quasi-Analytical Algorithm
====================================================

**XQAA** is a Python package implementing an improved Quasi-Analytical
Algorithm (QAA) for retrieving the **inherent optical properties (IOPs)** of
the ocean from remote-sensing reflectance. It reformulates the classical
Lee et al. QAA around the QSSA (Gordon) reflectance model, inverting the
non-water absorption in the blue and the particulate backscatter in the red.
Pure-water absorption and the Loisel+2023 reference dataset are loaded through
`ocpy <https://github.com/ocean-colour/ocpy>`_.

What XQAA does
--------------

* **A single-call retrieval** — :func:`xqaa.retrieve.iops_from_Rrs` takes a
  wavelength grid, an ``Rrs`` spectrum, and an
  :class:`~xqaa.params.XQAAParams` configuration, and returns the non-water
  absorption ``anw`` and particulate backscatter ``bbp``.
* **A transparent inversion** — the QSSA quadratic is inverted analytically
  for ``D = a/bb`` at every wavelength (:mod:`xqaa.inversion`); the red and
  blue spectral limits then yield ``bbp`` and ``anw`` directly.
* **Configurable coefficients** — fixed Gordon constants by default, or
  wavelength-dependent B-splines fit to Loisel+2023
  (``coeff_source='bspline'``).
* **Offline tooling** — :mod:`xqaa.qssa.derive` (re)generates the packaged
  coefficient files from the reference dataset.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   installation
   usage
   algorithm
   api/index

Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
