
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils.signatures   as rus

from   base      import AtomBase
from   constants import MEMORY

# ------------------------------------------------------------------------------
#
class Memory (AtomBase) :
    """
    This Memory Synapse emulates a memory workload, i.e. it allocates
    a specified memory size.  It does not create nor consume any I/O to the
    allocated memory -- instead, it quits right after allocation.
    """

    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Memory')
    @rus.returns (rus.nothing)
    def __init__ (self) : 

        AtomBase.__init__ (self, MEMORY)


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Memory', list)
    @rus.returns (rus.nothing)
    def run (self, vals) : 

        size = vals[0]

        return self._run (size)


#-------------------------------------------------------------------------------

