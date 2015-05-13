

__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "LGPL.v3"


import os
import time
import errno
import psutil
import threading
import subprocess
import multiprocessing

import radical.utils              as ru
import radical.utils.logger       as rul
import radical.utils.signatures   as rus

from constants import UNKNOWN, COMPUTE, STORAGE, NETWORK


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
        self._uid   = ru.generate_id ("%-10s" % self._atype)
        self.logger = rul.getLogger ("radical.synapse.%s" % self._uid)


        # storage for temporary data and statistics
     #  self._tmpdir = "/scratch/synapse/" # FIXME
        self._tmpdir = "/tmp/"             # FIXME

        try:
            os.makedirs (self._tmpdir)
        except OSError as exc :
            if exc.errno == errno.EEXIST and os.path.isdir (self._tmpdir) :
                pass
            else: raise

        # create our C-based workload script in tmp space
        self._exe = "%s/synapse_%s"  %  (self._tmpdir, self._atype)

        # already have the tool?
        if  not os.path.isfile (self._exe) :

            # if not, we compile it on the fly...
            # Note that the program below will actually, for each flop, also create
            # 3 INTEGER OPs and 1 Branching instruction.
            code = open (os.path.dirname(__file__) + '/synapse_%s.c' % self._atype).read ()

            p = subprocess.Popen ("cc -x c -O0 -o %s -" % self._exe,
                                  shell=True,
                                  stdin=subprocess.PIPE, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            (pout, perr) = p.communicate (code)

            if  p.returncode :
                raise Exception("Couldn't create %s: %s : %s" % (self._atype, pout, perr))

        # start worker process
        self._work_queue   = multiprocessing.Queue ()
        self._result_queue = multiprocessing.Queue ()

        self._proc  = multiprocessing.Process (target=self.work)
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
    def work (self) :

        while True :

            data = self._work_queue.get ()

            if data == None:
                # signal to finish
                return

            args = data
            cmd  = self._exe
            for arg in args:
                cmd += " %s" % str(arg)

          # print "start %-10s (%s) (%s)" % (self._atype, self._uid, cmd)

            t_start = time.time ()
            proc    = subprocess.Popen ("%s" % cmd, 
                                        shell=True,
                                        stdin=subprocess.PIPE, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)

            pout, perr = proc.communicate ()
            info       = {'timer' : float("%3.2f" % (time.time () - t_start)),
                          'ret'   : int(proc.returncode), 
                          'out'   : pout, 
                          'err'   : perr}

            self._result_queue.put (info)


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

