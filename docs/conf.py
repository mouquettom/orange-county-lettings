# Configuration file for the Sphinx documentation builder.

import os
import sys

import django


# -- Django setup ------------------------------------------------------------

# Add the project root directory to Python's import path.
sys.path.insert(0, os.path.abspath('..'))

# Tell Django which settings module to use.
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'oc_lettings_site.settings',
)

# Initialize Django so Sphinx can import models, views, etc.
django.setup()


# -- Project information -----------------------------------------------------

project = 'Orange County Lettings'
copyright = '2026, Tom Mouquet'
author = 'Tom Mouquet'
release = '1.0'


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
]

language = 'fr'


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
