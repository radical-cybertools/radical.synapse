
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


from   _atoms    import atom_compute_asm
from   _atoms    import atom_compute
from   base      import AtomBase
from   constants import COMPUTE

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
    def __init__ (self): 

        AtomBase.__init__ (self, COMPUTE)


    # --------------------------------------------------------------------------
    #
    def _verify(self, vals): 

        assert ('flops' in vals or 'time' in vals)

        # FIXME: empirical tuning factor toward 1 MFLOP
        if 'flops' in vals:
            vals['flops'] = int(vals['flops'] * 0.6)


    # --------------------------------------------------------------------------
    #
    def _emulate (self, vals): 

        try:
            # TODO: switch between flops and time emulation
          # print "atom_compute (%s)" % vals['flops']
            atom_compute_asm (vals['flops'])

        except Exception as e:
            print "com atom error: %s" % e


#-------------------------------------------------------------------------------

