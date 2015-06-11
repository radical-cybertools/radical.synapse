
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils.signatures   as rus

from   _atoms    import atom_compute_asm
from   _atoms    import atom_compute
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
    def emulate (self, vals) : 

        print 'cpu: %s' % vals

        ops = int(vals[0] * 0.6)

        # remove a empirical overhead
      # ops -= int(ops/100*OVERHEAD)
        self._run (ops)


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Compute', int)
    @rus.returns (rus.nothing)
    def _emulate (self, ops) : 

        atom_compute_asm (ops)


#-------------------------------------------------------------------------------

