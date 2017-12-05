
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


from   _atoms    import atom_compute_asm, atom_simple_adder, atom_mat_mult
from   _atoms    import atom_compute
from   base      import AtomBase
from   constants import COMPUTE, MATRIX_SIZE

OVERHEAD = 20   # in %

# ------------------------------------------------------------------------------
#
class Compute (AtomBase):
    """
    This Compute Synapse emulates a compute workload, i.e. it consumes
    a specified number of floating point operations.
    """

    # --------------------------------------------------------------------------
    #
    def __init__ (self, kernel_name=None): 

        AtomBase.__init__ (self, COMPUTE)
        self.kernel_name = kernel_name


    # --------------------------------------------------------------------------
    #
    def _verify(self, vals): 

        assert ('flops' in vals or 'time' in vals)

        # FIXME: empirical tuning factor toward 1 MFLOP

        #vals['flops'] = int(vals.get('flops', 0) * 0.6)
        #vals['time']  = int(vals.get('time',  0)      )
        
        vals['flops'] = int(vals.get('flops', 0))
        vals['time']  = int(vals.get('time', 0))


    # --------------------------------------------------------------------------
    #
    def _emulate (self, vals): 

        #try:
            # TODO: switch between flops and time emulation
          # print "atom_compute (%s)" % vals['flops']

        if not self.kernel_name:
            print "Calling regular atom"
            atom_compute_asm (vals['flops'], vals['time'])
        
        elif self.kernel_name == "adder":
            print "Calling atom simple_adder"
            atom_simple_adder(vals['flops'])
            
        elif self.kernel_name == "matmult":
            print "Calling atom mat_mult"
            atom_mat_mult(vals['flops'], MATRIX_SIZE)

        #except Exception as e:
        #    print "com atom error: %s" % e


#-------------------------------------------------------------------------------

