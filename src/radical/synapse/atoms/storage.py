
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils as ru


from   _atoms    import atom_storage
from   base      import AtomBase
from   constants import STORAGE

# ------------------------------------------------------------------------------
#
class Storage (AtomBase):
    """
    This Storage Synapse emulates a storage workload, i.e. it allocates
    a specified storage size on disk.  It creates only minimal I/O to the
    allocated storage, to ensure that the full amount has been allocated.
    """

    # --------------------------------------------------------------------------
    #
    def __init__ (self): 

        AtomBase.__init__ (self, STORAGE)


    # --------------------------------------------------------------------------
    #
    def _verify(self, vals): 

        # FIXME: get from profile, application
        vals['src'] = "/tmp/synapse_storage.in"
        vals['tgt'] = "/tmp/synapse_storage.%(pid)s.out"

        assert( ('rsize' in vals and 'src' in vals) or
                ('wsize' in vals and 'tgt' in vals)  )


    # --------------------------------------------------------------------------
    #
    def _emulate (self, vals):

        vals['src'] = vals['src'] % { 'tmp' : self._tmpdir, 'pid' : self._pid   }
        vals['tgt'] = vals['tgt'] % { 'tmp' : self._tmpdir, 'pid' : self._pid   }

        src   =     vals.get('src')
        rsize = int(vals.get('rsize', 0))
        tgt   =     vals.get('tgt')
        wsize = int(vals.get('wsize', 0))

        try:
            atom_storage(src, rsize, tgt, wsize)

        except Exception as e:
            print "sto atom error: %s" % e
            ru.cancel_main_thread()


#-------------------------------------------------------------------------------

