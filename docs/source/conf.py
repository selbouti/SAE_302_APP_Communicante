# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys

sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../client'))
sys.path.insert(0, os.path.abspath('../../serveur'))



project = 'SAE_302_APP_Communicante'
copyright = '2025, Roland,Soufiane,Samson,Sahlma'
author = 'Roland,Soufiane,Samson,Sahlma'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
'sphinx.ext.todo',
'sphinx.ext.mathjax',
'sphinx.ext.ifconfig',
'sphinx.ext.autodoc',
'sphinx.ext.viewcode',
]

autodoc_mock_imports = [
    "flask",
    "flask_cors",
    "PyQt5",
    "PyQt5.QtWidgets",
    "PyQt5.QtCore",
    "PyQt5.QtGui",
    "icalendar",
]

highlight_language = 'python'
pygments_style = 'sphinx'

templates_path = ['_templates']
exclude_patterns = []

language = 'french'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
html_css_files = [
    'custom.css',
]
