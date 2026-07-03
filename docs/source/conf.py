"""Configuration file for the XQAA Sphinx documentation builder.

See https://www.sphinx-doc.org/en/master/usage/configuration.html for the full
list of built-in configuration values.
"""

import os
import sys

# Make the xqaa package importable for autodoc. conf.py lives at
# docs/source/, so the repository root is two levels up.
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'XQAA'
copyright = '2026, J. Xavier Prochaska'
author = 'J. Xavier Prochaska'

try:                                   # single-source the version from the package
    import xqaa
    release = xqaa.__version__
except Exception:
    release = '0.1.dev0'
version = '.'.join(release.split('.')[:2])

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',         # NumPy / Google style docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
master_doc = 'index'

# -- Autodoc / autosummary ---------------------------------------------------

autosummary_generate = True

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
    'show-inheritance': True,
}
autodoc_typehints = 'description'      # built-in (no sphinx-autodoc-typehints dep)

# Mock the git-only sibling package so the docs build without installing it
# on the RTD runner. xqaa.retrieve and xqaa.qssa.derive import ocpy (pure-water
# absorption and the Loisel+2023 reference dataset).
autodoc_mock_imports = ['ocpy']

# Napoleon settings
napoleon_numpy_docstring = True
napoleon_google_docstring = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_ivar = True

# -- Intersphinx -------------------------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}

# -- HTML output -------------------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'titles_only': False,
    'style_nav_header_background': '#2980B9',
}
