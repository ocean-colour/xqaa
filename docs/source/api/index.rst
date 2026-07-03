=============
API reference
=============

Auto-generated documentation for the ``xqaa`` package.

Retrieval
=========

The top-level entry point: retrieve ``anw`` and ``bbp`` from an ``Rrs``
spectrum.

.. automodule:: xqaa.retrieve
   :members:

Geometric
=========

Above- to sub-surface reflectance conversion.

.. automodule:: xqaa.geometric
   :members:

Inversion
=========

The QSSA quadratic inversion and the red/blue-limit IOP solvers.

.. automodule:: xqaa.inversion
   :members:

Parameters
==========

.. automodule:: xqaa.params
   :members:

QSSA I/O
========

Filenames and loaders for the packaged coefficient files under
``xqaa/data/``.

.. automodule:: xqaa.qssa.io
   :members:

QSSA derivation
===============

Offline tooling that (re)generates the packaged coefficient files from the
reference dataset (requires ``ocpy``).

.. automodule:: xqaa.qssa.derive
   :members:
