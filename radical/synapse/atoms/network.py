
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils.signatures   as rus

from   base      import AtomBase
from   constants import NETWORK

# ------------------------------------------------------------------------------
#
class Network (AtomBase) :
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
    @rus.takes   ('Network')
    @rus.returns (rus.nothing)
    def __init__ (self) : 

        AtomBase.__init__ (self, NETWORK)


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('Network', dict)
    @rus.returns (rus.nothing)
    def run (self, info) : 

        self._proc = None

        if  not 'type' in info :
            print "need 'type' flags (server/client) to run network load"
            return

        if  not 'mode' in info :
            print "need 'mode' flags (send/recv) to run network load"
            return

        if  not 'port' in info :
            print "need 'port' flag to run network load"
            return

        typ  = info['type']
        mode = info['mode']
        port = info['port']
        host = "nohost"
        n    = 1

        if 'host' in info : host = info['host']
        if 'n'    in info : n    = info['n']

        if  typ == 'client' and not host :
            print "network server needs host and port"
            return

        self._run (typ, mode, host, port, n)


#-------------------------------------------------------------------------------

