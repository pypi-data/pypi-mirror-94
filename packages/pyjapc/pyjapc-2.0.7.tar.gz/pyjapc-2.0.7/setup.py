import sys

# XXX This if statement lets you actually build the package
if not 'sdist' in sys.argv:
    sys.exit("""
=========================================

`pyjapc` is now only available for installation via
the CERN Acc-Py package index.

Please see the CERN internal wiki at https://wikis.cern.ch/x/iQ2sC for details
of how to do this.

=========================================

""")

from distutils.core import setup

setup(
    name="pyjapc",
    version="2.0.7",
    description="Removed package from PyPI"
)
