
__author__    = "Radical.Utils Development Team (Andre Merzky, Ole Weidner)"
__copyright__ = "Copyright 2013, RADICAL@Rutgers"
__license__   = "MIT"


import os
import radical.utils        as ru
import radical.utils.logger as rul


# ------------------------------------------------------------------------------

SYNAPSE_DBURL = os.environ.get ('SYNAPSE_DBURL', 'mongodb://localhost:27017/')

from synapsify import synapsify
from synapsify import NOTHING
from synapsify import PROFILE
from synapsify import EMULATE

from utils     import profile_command
from utils     import emulate_command


# ------------------------------------------------------------------------------


pwd     = os.path.dirname (__file__)
root    = "%s/.." % pwd
short_version, long_version, branch = ru.get_version ([root, pwd])
version = long_version

# FIXME: the logger init will require a 'classical' ini based config, which is
# different from the json based config we use now.   May need updating once the
# radical configuration system has changed to json
_logger = rul.logger.getLogger  ('synapse')
_logger.info ('synapse         version: %s' % version)


# ------------------------------------------------------------------------------

