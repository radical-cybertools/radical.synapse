
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils as ru


from   _atoms    import atom_memory
from   base      import AtomBase
from   constants import MEMORY

# ------------------------------------------------------------------------------
#
class Memory (AtomBase):
    """
    This Memory Synapse emulates a memory workload, i.e. it allocates
    a specified memory size.  It does not create nor consume any I/O to the
    allocated memory -- instead, it quits right after allocation.
    """

    # --------------------------------------------------------------------------
    #
    def __init__ (self): 

        AtomBase.__init__ (self, MEMORY)


    # --------------------------------------------------------------------------
    #
    def _verify(self, vals): 

        assert ('size' in vals)


    # --------------------------------------------------------------------------
    #
    def _emulate (self, vals): 

        try:
         # print "atom_memorye (%s)" % vals['size']
            atom_memory (int(vals['size']))

        except Exception as e:
            print "mem atom error: %s" % e
            ru.cancel_main_thread()



#-------------------------------------------------------------------------------

