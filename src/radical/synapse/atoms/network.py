
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils as ru


from   _atoms    import atom_network
from   base      import AtomBase
from   constants import NETWORK

# ------------------------------------------------------------------------------
#
class Network (AtomBase):
    """
    This Network Synapse emulates a network workload.  It operates in either one
    of two modes: receive or send.  On receive, the synapse will listen on
    a given port (forever), and on any incoming connection will read data until
    the connection is closed from the sending end.  All data are immediately
    discarded.  Reading happens in 1MB chunks.
    On sending, the synapse will (forever) attempt to contact a receiver given 
    port, will send the given amount of data in 1MB chunk, and will then close
    the connection.
    """

    # --------------------------------------------------------------------------
    #
    def __init__ (self): 

        AtomBase.__init__ (self, NETWORK)


    # --------------------------------------------------------------------------
    #
    def _verify(self, vals): 

        self._proc = None

        assert('type' in vals)
        assert('mode' in vals)
        assert('port' in vals)

        typ  =     vals['type']
        mode =     vals['mode']
        port = int(vals['port'])
        host =     vals.get('size')
        size = int(vals.get('size', 1))

        assert(typ == 'client' or host)


    # --------------------------------------------------------------------------
    #
    def _emulate (self, vals):

        typ  =     vals['type']
        mode =     vals['mode']
        port = int(vals['port'])
        host =     vals.get('size')
        size = int(vals.get('size', 1))

        try:
            atom_network (typ, mode, host, port, size)

        except Exception as e:
            print "net atom error: %s" % e
            ru.cancel_main_thread()


#-------------------------------------------------------------------------------

