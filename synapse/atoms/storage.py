
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

        # workload property for this atom
        self.load_storage = 1000

        # create our C-based workload script in tmp space
        self._storage_exe = "%s/synapse_storage" % self._tmpdir

        # already have the storage tool?
        if  not os.path.isfile (self._storage_exe) :

            # if not, we compile it on the fly...
            # Note that the program below will actually, for each flop, also create
            # 3 INTEGER OPs and 1 Branching instruction.
            storage_code = open (os.path.dirname(__file__) + '/synapse_storage.c').read ()

            p = subprocess.Popen ("cc -x c -O0 -o %s -" % self._storage_exe,
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

        n_storage = 1

        if  'n_storage' in info : n_storage = info['n_storage']


        self._proc = multiprocessing.Process (target=self.work_storage,
            args=(n_storage,))

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
    def work_storage (self, n_storage) :
        """
        allocate requested amount of storage
        """

        print "start storage"

        p = subprocess.Popen ("%s %d" % (self._storage_exe, n_storage), 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        (pout, perr) = p.communicate ()

        if  pout: print pout
        if  perr: print perr

        print "stop  storage"

#
#-------------------------------------------------------------------------------

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

