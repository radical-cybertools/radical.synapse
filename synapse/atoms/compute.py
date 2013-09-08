
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"

MEMORY = "Memory"
FLOPS  = "Flops"


import os
import subprocess

import saga.utils.signatures   as sus

from base      import AtomBase
from constants import COMPUTE

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

        # create our C-based workload script in tmp space
        
        flops_file = "%s/flops" % self._tmpdir

        if  os.path.isfile (flops_file) :
            # already have the flops tool
            return

        # if not, we compile it on the fly...
        flops = """

#include <stdlib.h>

int main()
{
  long int i, I = atol (getenv ("ITER")) * 1000000;
  double   f = 1.0;

  for (i = 0; i < I; i++ )
  {
    f = f * 1.000000000001;
  }
}

"""

        p = subprocess.Popen ("cc -x c -O0 -o %s/flops -" % self._tmpdir, 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        (pout, perr) = p.communicate (flops)
        if  pout: print pout
        if  perr: print perr



    # --------------------------------------------------------------------------
    #
    @sus.takes   ('Compute')
    @sus.returns (sus.nothing)
    def work (self) :

        print "start work"
        p = subprocess.Popen ("ITER=1000 %s/flops -" % self._tmpdir, 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        (pout, perr) = p.communicate ()
        if  pout: print pout
        if  perr: print perr
        print "stop  work"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

