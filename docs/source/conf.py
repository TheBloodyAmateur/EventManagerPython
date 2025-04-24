# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EventManagerPy'
copyright = '2025, Botan Celik'
author = 'Botan Celik'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

import os
import sys

# Include the src/ folder, NOT EventManager/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']

html_theme = 'sphinx_rtd_theme'

autodoc_member_order = "bysource"



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
