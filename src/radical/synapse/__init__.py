
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

pwd     = os.path.dirname (__file__)
root    = "%s/.." % pwd
version, version_detail, version_branch, sdist_name, sdist_path = ru.get_version ([root, pwd])

_logger = ru.get_logger('radical.synapse')


# ------------------------------------------------------------------------------

