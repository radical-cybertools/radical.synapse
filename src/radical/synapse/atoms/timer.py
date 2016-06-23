
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import radical.utils as ru


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
    def __init__(self): 

        AtomBase.__init__(self, TIME)


    # --------------------------------------------------------------------------
    #
    def _verify(self, vals): 

        assert('real' in vals)


    # --------------------------------------------------------------------------
    #
    def _emulate(self, vals): 

        try:
            atom_time(vals['real'])

        except Exception as e:
            print "time atom error: %s" % e
            ru.cancel_main_thread()


#-------------------------------------------------------------------------------

