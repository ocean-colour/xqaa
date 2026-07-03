============
Installation
============

XQAA targets **Python ≥ 3.10** and is developed in the ``ocean14`` conda
environment.

From source
-----------

.. code-block:: bash

   git clone https://github.com/ocean-colour/xqaa.git
   cd xqaa
   pip install -e .

Sibling package
---------------

XQAA relies on one sibling package it does not own for pure-water absorption
and the Loisel+2023 reference dataset. It is not on PyPI, so install it from
source (the pinned ``requirements.txt`` pulls it from the tip of ``main``):

.. code-block:: bash

   pip install -r requirements.txt

* `ocpy <https://github.com/ocean-colour/ocpy>`_ — pure-water absorption
  (``ocpy.water.absorption``) and the Loisel+2023 Hydrolight dataset
  (``ocpy.hydrolight.loisel23``).

The remaining runtime dependencies (numpy, scipy, pandas, matplotlib) are
standard and installed automatically with the package.

Running the tests
-----------------

The unit tests for the geometric conversion, the quadratic inversion, the
parameter dataclass, and the packaged B-spline I/O run anywhere; the
end-to-end retrieval test imports ``ocpy`` and skips automatically when it is
absent:

.. code-block:: bash

   pytest -q
