

__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import os
import time
import errno
import psutil
import threading
import subprocess
import Queue

import radical.utils              as ru
import radical.utils.logger       as rul


# ------------------------------------------------------------------------------
#
class AtomBase (object):

    # --------------------------------------------------------------------------
    #
    def __init__  (self, atype):

        self._atype = atype
        self._pid   = os.getpid ()
        self._uid   = ru.generate_id ("%s" % self._atype)
        self.logger = ru.get_logger('radical.synapse.self._uid')

        # storage for temporary data and statistics
     #  self._tmpdir = "/scratch/synapse/" # FIXME
        self._tmpdir = "/tmp/"             # FIXME

        try:
            os.makedirs (self._tmpdir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir (self._tmpdir):
                pass
            else: raise


        # start worker process
        self._work_queue   = Queue.Queue ()
        self._result_queue = Queue.Queue ()

        self._term  = threading.Event()
        self._proc  = threading.Thread (target=self.run)
        self._proc.start ()


    # --------------------------------------------------------------------------
    #
    def __str__  (self):

        return self._uid


    # --------------------------------------------------------------------------
    #
    def run (self):

        try:

            while not self._term.is_set():

                vals = self._work_queue.get()
              # print " === vals: %s" % vals

                if not vals:
                    # signal to finish
                    self._result_queue.put (True)
                    return

              # print "emulate %-20s: %s" % (self, vals)
                self._emulate(vals)
                self._result_queue.put (True)


        except Exception as e:
            print "main loop error in atom driver: %s" % e
            raise


    # --------------------------------------------------------------------------
    #
    def emulate(self, vals):

        try:
            self._verify(vals)
            print "emulate  %s" % vals
            self._work_queue.put(vals)

        except Exception as e:
            print 'emulation error: invalid data: %s' % vals
            ru.cancel_main_thread()


    # --------------------------------------------------------------------------
    #
    def wait (self):

        return self._result_queue.get ()


    # --------------------------------------------------------------------------
    #
    def stop (self):

        self._term.set()
        self._work_queue.put (None) # signal finish

        if  self._proc:
            self._proc.join ()


    # --------------------------------------------------------------------------
    #
    def _verify(self, vals):

        raise NotImplementedError('%s atom misses _verify()' % self._atype)


    # --------------------------------------------------------------------------
    #
    def _emulate(self, vals):

        raise NotImplementedError('%s atom misses _emulate()' % self._atype)


# ------------------------------------------------------------------------------

