"""
PIPIT
A simple package to design shuffled protein sequences to interupt function.
"""

# Add imports here
from .shuffle import *
from .backend import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
