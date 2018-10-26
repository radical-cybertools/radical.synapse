
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2013, RADICAL@Rutgers"
__license__   = "MIT"



# ------------------------------------------------------------------------------

from synapsify import synapsify
from synapsify import NOTHING
from synapsify import PROFILE
from synapsify import EMULATE

from synapse   import profile
from synapse   import emulate
from synapse   import execute



# ------------------------------------------------------------------------------
#

import os
import radical.utils as ru

_mod_root = os.path.dirname (__file__)

version_short, version_detail, version_base, \
               version_branch, sdist_name,   \
               sdist_path = ru.get_version(_mod_root)
version = version_short
_logger = ru.get_logger('radical.synapse')


# ------------------------------------------------------------------------------

