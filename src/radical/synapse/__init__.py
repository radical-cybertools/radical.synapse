
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2013, RADICAL@Rutgers"
__license__   = "MIT"


# ------------------------------------------------------------------------------
# we *first* import radical.utils, so that the monkeypatching of the logger has
# a chance to kick in before the logging module is pulled by any other 3rd party
# module, and also to monkeypatch `os.fork()` for the `atfork` functionality
#
import os            as _os
import radical.utils as _ru


# ------------------------------------------------------------------------------
#
from .synapsify import synapsify
from .synapsify import NOTHING
from .synapsify import PROFILE
from .synapsify import EMULATE

from .synapse   import profile
from .synapse   import emulate
from .synapse   import execute


# ------------------------------------------------------------------------------
#
# get version info
#
_mod_root = _os.path.dirname (__file__)

version_short, version_base, version_branch, version_tag, version_detail \
             = _ru.get_version(_mod_root)
version      = version_short
__version__  = version_detail


# ------------------------------------------------------------------------------

