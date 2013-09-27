
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import os
import multiprocessing
import subprocess

import saga.utils.signatures   as sus

from   base      import AtomBase
from   constants import MEMORY

# ------------------------------------------------------------------------------
#
class Memory (AtomBase) :
    """
    This Memory Synapse emulates a memory workload, i.e. it allocates
    a specified memory size.  It does not create nor consume any I/O to the
    allocated memory -- instead, it quits right after allocation.
    """

    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Memory', 
                  sus.optional (dict))
    @sus.returns (sus.nothing)
    def __init__ (self, info={}) : 

        AtomBase.__init__ (self, MEMORY, info)

        # create our C-based workload script in tmp space
        self._exe = "%s/synapse_memory" % self._tmpdir

        # already have the memory tool?
        if  not os.path.isfile (self._exe) :

            # if not, we compile it on the fly...
            # Note that the program below will actually, for each flop, also create
            # 3 INTEGER OPs and 1 Branching instruction.
            memory_code = open (os.path.dirname(__file__) + '/synapse_memory.c').read ()

            p = subprocess.Popen ("cc -x c -O0 -o %s -" % self._exe,
                                  shell=True,
                                  stdin=subprocess.PIPE, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            (pout, perr) = p.communicate (memory_code)

            if  p.returncode :
                raise Exception("Couldn't create memory: %s : %s" % (pout, perr))


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Memory', 
                  sus.optional (dict))
    @sus.returns (sus.nothing)
    def run (self, info={}) : 

        n = 1

        if 'n' in info : n = info['n']

        self._proc = multiprocessing.Process (target=self.work, args=(n,))
        self._proc.start ()


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Memory')
    @sus.returns (sus.nothing)
    def wait (self) :

        self._proc.join ()



    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Memory')
    @sus.returns (sus.nothing)
    def work (self, n) :
        """
        allocate requested amount of memory
        """

        print "start memory %d" % n

        p = subprocess.Popen ("%s %d" % (self._exe, n), 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        (pout, perr) = p.communicate ()

        if  pout: print pout
        if  perr: print perr

        print "stop  memory"

#
#-------------------------------------------------------------------------------

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

