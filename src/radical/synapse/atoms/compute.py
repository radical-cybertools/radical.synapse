
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
    @rus.takes   ('Compute', list)
    @rus.returns (rus.nothing)
    def run (self, vals) : 

        ops = vals[0]

        # remove a empirical overhead
      # ops -= int(ops/100*OVERHEAD)
        self._run (ops)


#-------------------------------------------------------------------------------

