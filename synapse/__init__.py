
__author__    = "Radical.Utils Development Team (Andre Merzky, Ole Weidner)"
__copyright__ = "Copyright 2013, RADICAL@Rutgers"
__license__   = "MIT"


import os
import radical.utils.logger as rul


# ------------------------------------------------------------------------------

SYNAPSE_DBURL = 'mongodb://ec2-184-72-89-141.compute-1.amazonaws.com:27017/'

from synapsify import synapsify
from synapsify import NOTHING
from synapsify import PROFILE
from synapsify import EMULATE

from utils     import profile_command
from utils     import emulate_command


# ------------------------------------------------------------------------------

version = open (os.path.dirname (os.path.abspath (__file__)) + "/VERSION", 'r').read().strip()
_logger = rul.logger.getLogger  ('synapse')
_logger.info                    ('synapse         version: %s' % version)


# ------------------------------------------------------------------------------

