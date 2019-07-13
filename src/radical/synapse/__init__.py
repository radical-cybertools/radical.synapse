
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

pwd  = os.path.dirname (__file__)
root = "%s" % pwd
version_short, version_detail, version_base, \
        version_branch, sdist_name, sdist_path = ru.get_version(paths=[root])
version = version_short

logger = ru.Logger('radical.synapse')
logger.info('radical.synapse      version: %s' % version_detail)

# ------------------------------------------------------------------------------

