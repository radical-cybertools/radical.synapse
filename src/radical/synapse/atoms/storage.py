
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils.signatures   as rus

from   base      import AtomBase
from   constants import STORAGE

# ------------------------------------------------------------------------------
#
class Storage (AtomBase) :
    """
    This Storage Synapse emulates a storage workload, i.e. it allocates
    a specified storage size on disk.  It creates only minimal I/O to the
    allocated storage, to ensure that the full amount has been allocated.
    """

    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Storage')
    @rus.returns (rus.nothing)
    def __init__ (self) : 

        AtomBase.__init__ (self, STORAGE)


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Storage', dict)
    @rus.returns (rus.nothing)
    def run (self, info) : 

        t = "/scratch/synapse/synapse.%p.storage"
        n = 1

        if  'tgt' in info : t = info['tgt']
        if  'n'   in info : n = info['n']

        tgt = t % { 'tmp' : self._tmpdir, 'pid' : self._pid }

        self._run (tgt, n)


#-------------------------------------------------------------------------------

