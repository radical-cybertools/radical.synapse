
__author__    = "Radical.Utils Development Team (Andre Merzky, Ole Weidner)"
__copyright__ = "Copyright 2013, RADICAL@Rutgers"
__license__   = "MIT"


import os

import radical.utils.logger as rul



# ------------------------------------------------------------------------------

from synapsify import synapsify
from synapsify import NOTHING
from synapsify import PROFILE
from synapsify import EMULATE

from synapse   import profile_function
from synapse   import profile_command
from synapse   import emulate_command

from synapse   import get_mem_usage, get_io_usage
from synapse   import human_to_number
from synapse   import number_to_human
from synapse   import PREFIX_ISO
from synapse   import PREFIX_BIN


# ------------------------------------------------------------------------------


import os

_mod_root = os.path.dirname (__file__)

version        = open (_mod_root + "/VERSION",     "r").readline ().strip ()
version_detail = open (_mod_root + "/VERSION.git", "r").readline ().strip ()


# ------------------------------------------------------------------------------

_logger = rul.logger.getLogger  ('synapse')
_logger.info ('synapse         version: %s' % version)


# ------------------------------------------------------------------------------



