# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.append(os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "embestore"
copyright = "2023, Yoshi"
author = "Yoshi"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    # "sphinx.ext.autodoc",  # Core Sphinx library for auto html doc generation from docstrings
    # "sphinx.ext.autosummary",  # Create neat summary tables for modules/classes/methods etc
    "sphinx.ext.intersphinx",  # Link to other project's documentation (see mapping below)
    "numpydoc",
    "myst_parser",
]


source_suffix = {".rst": "restructuredtext", ".md": "markdown"}


numpydoc_show_class_members = False


# generate autosummary even if no references
autosummary_generate = False
autosummary_imported_members = False

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
