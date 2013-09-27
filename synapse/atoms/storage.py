
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import os
import multiprocessing
import subprocess

import saga.utils.signatures   as sus

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
    @sus.takes   ('Storage', 
                  sus.optional (dict))
    @sus.returns (sus.nothing)
    def __init__ (self, info={}) : 

        AtomBase.__init__ (self, STORAGE, info)

        # create our C-based workload script in tmp space
        self._exe = "%s/synapse_storage" % self._tmpdir

        # already have the storage tool?
        if  not os.path.isfile (self._exe) :

            # if not, we compile it on the fly...
            # Note that the program below will actually, for each flop, also create
            # 3 INTEGER OPs and 1 Branching instruction.
            storage_code = open (os.path.dirname(__file__) + '/synapse_storage.c').read ()

            p = subprocess.Popen ("cc -x c -O0 -o %s -" % self._exe,
                                  shell=True,
                                  stdin=subprocess.PIPE, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            (pout, perr) = p.communicate (storage_code)

            if  p.returncode :
                raise Exception("Couldn't create storage: %s : %s" % (pout, perr))


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Storage', 
                  sus.optional (dict))
    @sus.returns (sus.nothing)
    def run (self, info={}) : 

        t = "/tmp/synapse.%p.storage"
        n = 1

        if  'tgt' in info : t = info['tgt']
        if  'n'   in info : n = info['n']

        tgt = t % { 'tmp' : self._tmpdir, 'pid' : self._pid }


        self._proc = multiprocessing.Process (target=self.work, args=(tgt,n))
        self._proc.start ()


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Storage')
    @sus.returns (sus.nothing)
    def wait (self) :

        self._proc.join ()



    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Storage')
    @sus.returns (sus.nothing)
    def work (self, tgt, n) :
        """
        allocate requested amount of storage
        """

        print "start storage %s %d" % (tgt, n)

        p = subprocess.Popen ("%s %s %d" % (self._exe, tgt, n), 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        (pout, perr) = p.communicate ()

        if  pout: print pout
        if  perr: print perr

        print "stop  storage %s" % p.returncode

#
#-------------------------------------------------------------------------------

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

