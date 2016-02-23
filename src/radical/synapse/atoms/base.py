

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
import radical.utils.signatures   as rus


# ------------------------------------------------------------------------------
#
class AtomBase (object) :

    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase', 
                  basestring, 
                  dict)
    @rus.returns (rus.nothing)
    def __init__  (self, atype) :


        self._atype = atype
        self._pid   = os.getpid ()
        self._uid   = ru.generate_id ("%s" % self._atype)
        self.logger = ru.get_logger('radical.synapse.self._uid')

        # storage for temporary data and statistics
     #  self._tmpdir = "/scratch/synapse/" # FIXME
        self._tmpdir = "/tmp/"             # FIXME

        try:
            os.makedirs (self._tmpdir)
        except OSError as exc :
            if exc.errno == errno.EEXIST and os.path.isdir (self._tmpdir) :
                pass
            else: raise


        # start worker process
        self._work_queue   = Queue.Queue ()
        self._result_queue = Queue.Queue ()

        self._proc  = threading.Thread (target=self.run)
        self._proc.start ()


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (basestring)
    def __str__  (self) :

        return self._uid


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (rus.nothing)
    def run (self) :

        try:

            while True :

                data = self._work_queue.get ()

                if data == None:
                    # signal to finish
                    return

                print "emulate %-20s: %s" % (self, str(data))
                self._emulate (*data)
                self._result_queue.put (True)


        except Exception as e:
            print "main loop error in atom driver: %s" % e
            raise


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (rus.nothing)
    def _run (self, *args) : 

        self._work_queue.put (args)


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (dict)
    def wait (self) :

        return self._result_queue.get ()


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (rus.nothing)
    def stop (self) :

        self._work_queue.put (None) # signal finish

        if  self._proc :
            self._proc.join ()


# ------------------------------------------------------------------------------

