
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

import radical.utils        as ru
import radical.utils.logger as rul


pwd     = os.path.dirname (__file__)
root    = "%s/.." % pwd
version, version_detail, version_branch, sdist_name, sdist_path = ru.get_version ([root, pwd])

_logger = rul.logger.getLogger  ('radical.synapse')
_logger.info ('radical.synapse      version: %s' % version_detail)


# ------------------------------------------------------------------------------

