
__author__    = "Radical.Utils Development Team (Andre Merzky, Ole Weidner)"
__copyright__ = "Copyright 2013, RADICAL@Rutgers"
__license__   = "MIT"


import os
import radical.utils.logger as rul


# ------------------------------------------------------------------------------

version = open (os.path.dirname (os.path.abspath (__file__)) + "/VERSION", 'r').read().strip()
_logger = rul.logger.getLogger  ('synapse')

_logger.info ('synapse         version: %s' % version)


# ------------------------------------------------------------------------------

