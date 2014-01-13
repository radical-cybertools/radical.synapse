

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


        self.atype  = atype
        self.aid    = ru.generate_id ("%-10s" % atype)
        self.logger = rul.getLogger (self.aid)


        # storage for temporary data and statistics
        self.info    = None
        self._proc   = None
        self._uid    = os.getuid ()
        self._pid    = os.getpid ()
     #  self._tmpdir = "/tmp/synapse_%d_%d" % (self._uid, self._pid)
        self._tmpdir = "/tmp/synapse/" # FIXME
     #  self._tmpdir = "/scratch/synapse/" # FIXME


        try:
            os.makedirs (self._tmpdir)
        except OSError as exc :
            if exc.errno == errno.EEXIST and os.path.isdir (self._tmpdir) :
                pass
            else: raise

        # create our C-based workload script in tmp space
        self._exe = "%s/synapse_%s"  %  (self._tmpdir, atype)

        # already have the tool?
        if  not os.path.isfile (self._exe) :

            # if not, we compile it on the fly...
            # Note that the program below will actually, for each flop, also create
            # 3 INTEGER OPs and 1 Branching instruction.
            code = open (os.path.dirname(__file__) + '/synapse_%s.c' % atype).read ()

            p = subprocess.Popen ("cc -x c -O0 -o %s -" % self._exe,
                                  shell=True,
                                  stdin=subprocess.PIPE, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            (pout, perr) = p.communicate (code)

            if  p.returncode :
                raise Exception("Couldn't create %s: %s : %s" % (atype, pout, perr))


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (rus.nothing)
    def work (self, *args) :

        cmd = self._exe
        for arg in args :
            cmd += ' %s' % str(arg)

      # print "start %-10s (%s) (%s)" % (self.atype, self.aid, cmd)

        t_start = time.time ()

        mem = 0
      # p = subprocess.Popen ("/usr/bin/time -v perf stat %s" % cmd,
        p = subprocess.Popen ("%s" % cmd, 
                              shell=True,
                              stdin=subprocess.PIPE, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)

        pout, perr = p.communicate ()

        info = {'timer'    : float("%3.2f" % (time.time () - t_start)),
                'exitcode' : int(p.returncode), 
                'out'      : pout.split ('\n'), 
                'err'      : perr.split ('\n')}

        self._queue.put (info)


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (rus.nothing)
    def _run (self, *args) : 

        self._queue = multiprocessing.Queue ()
        self._proc  = multiprocessing.Process (target=self.work, args=args)
        self._proc.start ()


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (basestring)
    def __str__  (self) :

        return self.aid


    # --------------------------------------------------------------------------
    #
    @rus.takes   ('AtomBase')
    @rus.returns (float)
    def wait (self) :

        if  self._proc :
            self._proc.join ()

        if  not self.info :
            self.info = self._queue.get ()

        return self.info




