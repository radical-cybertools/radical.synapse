
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import os
import multiprocessing
import subprocess

import saga.utils.signatures   as sus

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
    @sus.takes   ('Network', 
                  sus.optional (dict))
    @sus.returns (sus.nothing)
    def __init__ (self, info={}) : 

        AtomBase.__init__ (self, NETWORK, info)

        # create our C-based workload script in tmp space
        self._exe = "%s/synapse_network" % self._tmpdir

        # already have the network tool?
        if  not os.path.isfile (self._exe) :

            # if not, we compile it on the fly...
            # Note that the program below will actually, for each flop, also create
            # 3 INTEGER OPs and 1 Branching instruction.
            network_code = open (os.path.dirname(__file__) + '/synapse_network.c').read ()

            p = subprocess.Popen ("cc -g -x c -O0 -o %s -" % self._exe,
                                  shell=True,
                                  stdin=subprocess.PIPE, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            (pout, perr) = p.communicate (network_code)

            if  p.returncode :
                raise Exception("Couldn't create network: %s : %s" % (pout, perr))


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Network', 
                  sus.optional (dict))
    @sus.returns (sus.nothing)
    def run (self, info={}) : 

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

        self._proc = multiprocessing.Process (target=self.work, 
                                              args=(typ, mode, host, port, n))
        self._proc.start ()


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Network')
    @sus.returns (sus.nothing)
    def wait (self) :

        if  self._proc :
            self._proc.join ()



    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Network')
    @sus.returns (sus.nothing)
    def work (self, typ, mode, host, port, n) :
        """
        use requested amount of network
        """

        print "start network %s %s %s %d %d" % (typ, mode, host, port, n)

        p = subprocess.Popen ("%s %s %s %s %d %d" % (self._exe, typ, mode, host, port, n), 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        (pout, perr) = p.communicate ()

        if  pout: print pout
        if  perr: print perr

        print "stop  network %s" % p.returncode

#
#-------------------------------------------------------------------------------

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

