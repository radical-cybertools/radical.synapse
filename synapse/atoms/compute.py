
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"

MEMORY = "Memory"
FLOPS  = "Flops"


import os
import multiprocessing
import subprocess

import saga.utils.signatures   as sus

from   base      import AtomBase
from   constants import COMPUTE

# ------------------------------------------------------------------------------
#
class Compute (AtomBase) :
    """
    This Compute Synapse emulates a compute workload, i.e. it allocates
    a specified memory size, and consumes a specified number of flops.  It does
    not create nor consume any I/O.
    """

    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Compute', 
                  sus.optional (dict))
    @sus.returns (sus.nothing)
    def __init__ (self, info={}) : 

        AtomBase.__init__ (self, COMPUTE, info)

        # workload property for this atom
        self.load_flops  = 1000
        self.load_malloc = 1000

        # create our C-based workload script in tmp space
        self._flops_exe  = "%s/synapse_flops"  % self._tmpdir
        self._malloc_exe = "%s/synapse_malloc" % self._tmpdir

        # already have the flops tool?
        if  not os.path.isfile (self._flops_exe) :

            # if not, we compile it on the fly...
            # Note that the program below will actually, for each flop, also create
            # 3 INTEGER OPs and 1 Branching instruction.
            flops_code = open (os.path.dirname(__file__) + '/synapse_flops.c').read ()

            p = subprocess.Popen ("cc -x c -O0 -o %s -" % self._flops_exe,
                                  shell=True,
                                  stdin=subprocess.PIPE, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            (pout, perr) = p.communicate (textwrap.dedent (flops_code))

            if  p.returncode :
                raise Exception("Couldn't create flops: %s : %s" % (pout, perr))



        # already have the malloc tool?
        if  not os.path.isfile (self._malloc_exe) :

            # if not, we compile it on the fly...
            # Note that the program below will actually, for each flop, also create
            # 3 INTEGER OPs and 1 Branching instruction.
            malloc_code = open (os.path.dirname(__file__) + '/synapse_malloc.c').read ()

            p = subprocess.Popen ("cc -x c -O0 -o %s -" % self._malloc_exe,
                                  shell=True,
                                  stdin=subprocess.PIPE, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            (pout, perr) = p.communicate (textwrap.dedent (malloc_code))

            if  p.returncode :
                raise Exception("Couldn't create malloc: %s : %s" % (pout, perr))


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Compute', 
                  sus.optional (dict))
    @sus.returns (sus.nothing)
    def work (self, info={}) : 

        n_malloc = 1
        n_flops  = 1

        if  'n_malloc' in info : n_malloc = info['n_malloc']
        if  'n_flops'  in info : n_flops  = info['n_flops']


        p_malloc = multiprocessing.Process (target=self.work_malloc, args=(n_malloc,))
        p_flops  = multiprocessing.Process (target=self.work_flops , args=(n_flops, ))

        p_malloc.start ()
        p_flops .start ()

        p_malloc.join ()
        p_flops .join ()


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Compute')
    @sus.returns (sus.nothing)
    def work_malloc (self, n_malloc) :
        """
        allocate requested amount of memory
        """

        print "start malloc"

        p = subprocess.Popen ("%s %d" % (self._malloc_exe, n_malloc), 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        (pout, perr) = p.communicate ()

        if  pout: print pout
        if  perr: print perr

        print "stop  malloc"


    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Compute')
    @sus.returns (sus.nothing)
    def work_flops (self, n_flops) :
        """
        run requested number of flops
        """

        print "start flops"

        p = subprocess.Popen ("%s %d" % (self._flops_exe, n_flops), 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        (pout, perr) = p.communicate ()

        if  pout: print pout
        if  perr: print perr

        print "stop  flops"

#
#-------------------------------------------------------------------------------

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

