# __init__.py

"""
__init__.py file for the `csvdeploy` library.
"""

# Package information for the library
__version__ = "0.1"
__author__ = "Tiago Tresoldi"
__email__ = "tiago.tresoldi@lingfil.uu.se"

# Build the namespace
from .common import read_plain_csv, load_config, read_data
from .render import render_site
