
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils.signatures   as rus

from   _atoms    import atom_time
from   base      import AtomBase
from   constants import TIME

# ------------------------------------------------------------------------------
#
class Time(AtomBase):
    """
    This Time Synapse emulates a an applications walltime behavior without
    consuming resources.
    """

    # --------------------------------------------------------------------------
    #
    @rus.takes  ('Time')
    @rus.returns(rus.nothing)
    def __init__(self): 

        AtomBase.__init__(self, TIME)


    # --------------------------------------------------------------------------
    #
    @rus.takes  ('Time', list)
    @rus.returns(rus.nothing)
    def emulate (self, vals): 

        print 'time: %s' % vals

        self._run(vals[0])


    # --------------------------------------------------------------------------
    #
    @rus.takes  ('Time', float)
    @rus.returns(rus.nothing)
    def _emulate(self, ops): 

        atom_time(ops)


#-------------------------------------------------------------------------------

