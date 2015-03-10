
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

        mode  = info.get ('mode',  'w')
        tgt   = info.get ('tgt',   None)
        size  = info.get ('size',  1024*1024)  # 2^20
        chunk = info.get ('chunk', 1024*1024)  # 2^20

        if  mode not in ['r', 'w']:
            raise ValueError ("invalid storage mode '%s'" % mode)

        if  not tgt:
            if  mode == 'r': raise ValueError ("need input source")
            else           : tgt = "/tmp/synapse/synapse.%(pid)s.storage"

        tgt = tgt % { 'tmp' : self._tmpdir, 
                      'pid' : self._pid   }

        self._run (mode, tgt, size, chunk)


#-------------------------------------------------------------------------------

