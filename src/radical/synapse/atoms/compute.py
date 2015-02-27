
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils.signatures   as rus

from   base      import AtomBase
from   constants import COMPUTE

OVERHEAD = 20   # in %

# ------------------------------------------------------------------------------
#
class Compute (AtomBase) :
    """
    This Compute Synapse emulates a compute workload, i.e. it consumes
    a specified number of floating point operations.
    """

    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Compute')
    @rus.returns (rus.nothing)
    def __init__ (self) : 

        AtomBase.__init__ (self, COMPUTE)


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Compute', dict)
    @rus.returns (rus.nothing)
    def run (self, info) : 

        n = 1

        if 'n' in info : n = info['n']

        # remove a empirical overhead
        n -= int(n/100*OVERHEAD)
        self._run (n)


#-------------------------------------------------------------------------------

