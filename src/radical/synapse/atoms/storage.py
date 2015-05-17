
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils.signatures   as rus

from   _atoms    import atom_storage
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
    @rus.takes   ('Storage', list)
    @rus.returns (rus.nothing)
    def emulate (self, vals) : 

        rsize = int(vals[0])
        wsize = int(vals[1])

      # f = open ("/tmp/l")
      # for i in range(10000000):
      #     data = f.read (10)
      # f.close()

        if  rsize: 
            # FIXME
            pass 
            # not yet supported
          # raise ValueError ("need input source (%s)" % read)
          # rsize = 0

        src = "/tmp/synapse_storage.%(pid)s.in"
        src = "/tmp/l" # FIXME
        tgt = "/tmp/synapse_storage.%(pid)s.out"

        src = tgt % { 'tmp' : self._tmpdir, 'pid' : self._pid   }
        tgt = tgt % { 'tmp' : self._tmpdir, 'pid' : self._pid   }

        self._run (src, rsize, tgt, wsize)


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Storage', basestring, int, basestring, int)
    @rus.returns (rus.nothing)
    def _emulate (self, src, rsize, tgt, wsize) : 

        atom_storage (src, rsize, tgt, wsize)


#-------------------------------------------------------------------------------

