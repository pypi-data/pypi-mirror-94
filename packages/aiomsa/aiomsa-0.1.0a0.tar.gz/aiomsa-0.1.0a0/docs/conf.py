# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import pathlib
import re

import aiohttp.web
from sphinx.ext.autodoc import between


# -- Module Remapping --------------------------------------------------------

aiohttp.web.Request.__module__ = "aiohttp.web"
aiohttp.web.Response.__module__ = "aiohttp.web"
aiohttp.web.RouteTableDef.__module__ = "aiohttp.web"


# -- Project information -----------------------------------------------------

HERE = pathlib.Path(__file__).parent.parent
txt = (HERE / "aiomsa" / "__init__.py").read_text("utf-8")
try:
    version = re.findall(r'^__version__ = "([^"]+)"\r?$', txt, re.M)[0]
except IndexError:
    raise RuntimeError("Unable to determine version.")

project = "aiomsa"
copyright = "2021, Facebook"
author = "Facebook"

# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- intersphinx configuration -----------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
}


# -- autodoc configuration ---------------------------------------------------

autodoc_member_order = "bysource"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]


def setup(app):
    app.connect("autodoc-process-docstring", between("^---$", exclude=True))
    return app
