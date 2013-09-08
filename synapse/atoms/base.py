
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import os
import errno
import threading

import saga.utils.logger       as sul
import saga.utils.signatures   as sus

from constants import UNKNOWN, COMPUTE, STORAGE, NETWORK, ANY

# ------------------------------------------------------------------------------
#
# use module level counter for unique IDs
#
idx = {}
idx[COMPUTE] = 0
idx[STORAGE] = 0
idx[NETWORK] = 0
idx[UNKNOWN] = 0

def _get_aid (atype) :

    if atype == COMPUTE : return ("compute_%06d" % idx[atype])
    if atype == STORAGE : return ("storage_%06d" % idx[atype])
    if atype == NETWORK : return ("network_%06d" % idx[atype])
    else                : return ("unknown_%06d" % idx[UNKNOWN])


# ------------------------------------------------------------------------------
#
class AtomBase (object) :

    # --------------------------------------------------------------------------
    #
    @sus.takes   ('AtomBase', 
                  int, 
                  sus.optional(dict))
    @sus.returns (sus.nothing)
    def __init__  (self, atype, info=None) :


        self.atype  = atype
        self.aid    = _get_aid (atype)
        self.logger = sul.getLogger (self.aid)


        # storage for temporary data and statistics
        self._uid    = os.getuid ()
        self._pid    = os.getpid ()
        self._tmpdir = "/tmp/synapse_%d_%d" % (self._uid, self._pid)
        self._tmpdir = "/tmp/synapse/" # FIXME


        try:
            os.makedirs (self._tmpdir)
        except OSError as exc :
            if exc.errno == errno.EEXIST and os.path.isdir (self._tmpdir) :
                pass
            else: raise





    # --------------------------------------------------------------------------
    #
    @sus.takes   ('AtomBase')
    @sus.returns (basestring)
    def __str__  (self) :

        return self.aid



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

