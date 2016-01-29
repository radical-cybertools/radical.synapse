
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2015, RADICAL@Rutgers"
__license__   = "MIT"

import re
import os
import signal
import select
import threading

import subprocess    as sp
import radical.utils as ru
import watcher_base  as wb


# ------------------------------------------------------------------------------
#
class WatcherCPU (wb.WatcherBase) :
    """
    This watcher mostly uses 'perf stat' to analyse program execution
    performance.  See [1] for an detailed introduction to perf.
    
    [1] http://www.brendangregg.com/perf.html
    """

    # --------------------------------------------------------------------------
    #
    def __init__ (self, pid):

        wb.WatcherBase.__init__(self, pid)

        self._data['cpu']             = dict()
        self._data['cpu']['sequence'] = list()


    # --------------------------------------------------------------------------
    #
    # FIXME: for some reasons, running w/o shell=True fails.   So we need to
    # take a detour to communicate the perf pid.  We should try to get rid of
    # the shelling...
    #
    def _pre_process (self, config):

        # sample rate is in samples/sec, we convert into time between samples in
        # milliseconds.  Minimum is 100 ms
        sample_time = 1 / config.get ('sample_rate', 1) * 1000
        sample_time = max(sample_time, 100)

        sample_cmd  = "sh -c 'perf stat -I %d -p %d & PID=$!; " % (sample_time, self._pid) \
                    + "echo $PID > /tmp/synapse.pid.cpu_sample.$PPID; " \
                    + "wait $PID'" 
        total_cmd   = "sh -c 'perf stat -v -p %d & PID=$!; " % (self._pid) \
                    + "echo $PID > /tmp/synapse.pid.cpu_total.$PPID; " \
                    + "wait $PID'" 

      # print sample_cmd
      # print total_cmd
        self._psam  = sp.Popen (sample_cmd,
                                stdout = sp.PIPE,
                                stderr = sp.STDOUT,
                                shell  = True)
        self._ptot  = sp.Popen (total_cmd,
                                stdout = sp.PIPE,
                                stderr = sp.STDOUT,
                                shell  = True)

        self._osam  = ""
        self._otot  = ""


    # --------------------------------------------------------------------------
    #
    def _sample (self, now):

        # to avoid the proc buffers to fill up, we need to continuously read
        # from the pipes.  We don't want to have this blocking though, so only
        # read if select tells us there are more data

        while (select.select([self._psam.stdout], [], [], 0)[0] != []):   
            data        = self._psam.stdout.read(1)
            self._osam += data

        while (select.select([self._ptot.stdout], [], [], 0)[0] != []):   
            data        = self._ptot.stdout.read(1)
            self._otot += data

    # --------------------------------------------------------------------------
    #
    def _post_process (self):

        # proc should be done now -- let it know.  But first make sure we are
        # listening on the pipes when it dies...
        perf_pid = int(open ('/tmp/synapse.pid.cpu_total.%s' % self._ptot.pid, 'r').read().strip())
        os.unlink ('/tmp/synapse.pid.cpu_total.%s' % self._ptot.pid)

        threading.Timer (1.0, os.kill, [perf_pid, signal.SIGINT]).start ()
        out = self._ptot.communicate()[0]

        self._parse_perf_total (self._otot + out)


        # now do the same for the sampling counters
        perf_pid = int(open ('/tmp/synapse.pid.cpu_sample.%s' % self._psam.pid, 'r').read().strip())
        os.unlink ('/tmp/synapse.pid.cpu_sample.%s' % self._psam.pid)

        threading.Timer (1.0, os.kill, [perf_pid, signal.SIGINT]).start ()
        out = self._psam.communicate()[0]

        self._parse_perf_sample (self._osam + out)


    # --------------------------------------------------------------------------
    # 
    def _finalize (self, info) :

        # efficiency  = cycles_used /  cycles_spent
        #             = cycles_used / (cycles_used + cycles_wasted)
        #             = 0..1
        # utilization = cycles_used /  cycles_max
        #             = 0..1
        #
        # In 'perf stat', stalled cycles + used cycles don't add up to spent
        # cycles (ie. usually gove more than 100%).  This is due to the fact
        # that different low level counter layers are used which can be
        # triggered by front- and backend stalls.  The used definitions
        # for utilization and efficiency may thus not exactly reflect the
        # naively expected definitions -- but they should nevertheless
        # result in a useful measure with similar bouncs as the naive
        # definition...
        #
        #  * http://stackoverflow.com/questions/22165299/

        fpc  = info['cpu']['flops_per_cycle']
        freq = info['cpu']['frequency']

        real = info['time']['real']

        ops  = info['cpu'].get('ops', 0)
        cns  = info['cpu'].get('cycles', 0)
        csf  = info['cpu'].get('cycles_stalled_front', 0)
        csb  = info['cpu'].get('cycles_stalled_back',  0)

        ctot = cns  + csf + csb
        cmax = freq * real
        cuse = ops  / fpc

        if real    : info['cpu']['real']        = real
        else       : info['cpu']['real']        = None

        if real    : info['cpu']['flops']       = ops / real
        else       : info['cpu']['flops']       = None

        if ctot    : info['cpu']['efficiency']  = cuse / (cuse + csf + csb)
        else       : info['cpu']['efficiency']  = None

        if cmax    : info['cpu']['utilization'] = cuse / cmax
        else       : info['cpu']['utilization'] = None
        

        # now we do the same for each sample, and use the time diff between
        # samples as real time.
        old = 0.0
        for ts,sample in info['cpu']['sequence']:

            real = ts - old
            old  = ts

            ops  = sample.get('ops', 0)
            cns  = sample.get('cycles', 0)
            csf  = sample.get('cycles_stalled_front', 0)
            csb  = sample.get('cycles_stalled_back',  0)

            ctot = cns  + csf + csb
            cmax = freq * real
            cuse = ops  / fpc

            if real    : sample['real']        = real
            else       : sample['real']        = None

            if real    : sample['flops']       = ops / real
            else       : sample['flops']       = None

            if ctot    : sample['efficiency']  = cuse / (cuse + csf + csb)
            else       : sample['efficiency']  = None

            if cmax    : sample['utilization'] = cuse / cmax
            else       : sample['utilization'] = None


    # --------------------------------------------------------------------------
    # 
    def _parse_perf_total (self, perf_out) :
    
        if  isinstance (perf_out, basestring) :
            perf_out = perf_out.split ('\n')
    
        # prepare to dig data from perf output lines
        perf_keys  = {# "CPUs utilized"           : "utilization",
                        "instructions"            : "ops",
                        "branches"                : "branches",
                        "branch-misses"           : "branch_misses",
                        "cycles"                  : "cycles",
                        "stalled-cycles-frontend" : "cycles_stalled_front",
                        "stalled-cycles-backend"  : "cycles_stalled_back",
                        "frontend cycles idle"    : "cycles_idle_front",
                        "backend  cycles idle"    : "cycles_idle_back",
                        "insns per cycle"         : "ops_per_cycle"}
        ored_keys   = '|'.join(perf_keys.keys()).replace (' ', '\s')
        perf_patstr = r"""
            ^(?P<lead>.*?\s+)            # lead-in
            (?P<val>[\d\.,]+)%%?         # value
            \s+                          # skip
            (?P<key>%s)                  # key
            \s*                          # skip
            (\[(?P<perc>[\d\.]+)%%\])?   # percentage (optional)
            \s*                          # skip
            (?P<rest>.*)$                # lead-out
        """ % ored_keys
        perf_pat = re.compile (perf_patstr, re.VERBOSE)
    
        # and go
        for line in perf_out :
    
            l = ru.ReString (line)
    
          # print "line: %s" % line
    
            while l // (perf_pat) :
    
                key  = perf_keys[l.get ('key')]
                val  =           l.get ('val')
                perc =           l.get ('perc', '-1.0')
    
                if  not perc :
                    perc = '-1.0'
    
              # print " ->  %s  %s  %s" % (key, val, perc)
    
                self._data['cpu']['%s'      % key] = float(val.replace  (',', ''))
                self._data['cpu']['%s_perc' % key] = float(perc.replace (',', ''))
    
              # print "rest: %s" % l.get ('rest')
                l = ru.ReString (l.get ('rest'))
    
        # must haves
        if not self._data['cpu'].get('ops'                 ) : self._data['cpu']['ops'                  ] = 1
        if not self._data['cpu'].get('cycles_idle_front'   ) : self._data['cpu']['cycles_idle_front'    ] = 0
        if not self._data['cpu'].get('cycles_idle_back'    ) : self._data['cpu']['cycles_idle_back'     ] = 0
        if not self._data['cpu'].get('cycles_stalled_front') : self._data['cpu']['cycles_stalled_front' ] = 0
        if not self._data['cpu'].get('cycles_stalled_back' ) : self._data['cpu']['cycles_stalled_back'  ] = 0
    
        self._data['cpu']['efficiency']  = self._data['cpu']['ops']                       \
                              / ( self._data['cpu']['ops']                   \
                                + self._data['cpu']['cycles_stalled_front']  \
                                + self._data['cpu']['cycles_stalled_back']   \
                                )
    
        # also determine the theoretical number of FLOPS, which is calculated as
        #   FLOPS = #cores * #cycles/sec * flops/cycle
        # where flops/cycle are assumed to be 4 (see wikipedia on FLOPS).  We assume
        # that the watched process uses only one core, so we calculate the number
        # for one core only, but also report the number of cores.
        
    
    
    # --------------------------------------------------------------------------
    # 
    def _parse_perf_sample (self, perf_out) :
    
        if  isinstance (perf_out, basestring) :
            perf_out = perf_out.split ('\n')
    
        # prepare to dig data from perf output lines
        perf_keys  = {# "task-clock"              : "utilization",
                      # "context-switches"        : "context_switches",
                      # "cpu-migrations"          : "cpu_migrations",
                        "instructions"            : "ops",
                      # "page-faults"             : "page_faults",
                        "branches"                : "branches",
                        "branch-misses"           : "branch_misses",
                        "cycles"                  : "cycles",
                        "stalled-cycles-frontend" : "cycles_stalled_front",
                        "stalled-cycles-backend"  : "cycles_stalled_back"}
        ored_keys   = '|'.join(perf_keys.keys()).replace (' ', '\s')
        perf_patstr = r"""
           ^(?P<lead>\s+)                # lead-in
            (?P<time>[\d\.,]+)           # timestamp
            \s+                          # skip
            (?P<val>[\d\.,]+)            # value (ignore warnings)
            \s+                          # skip
            (?P<key>%s)                  # key
            \s*                          # skip
            (\[(?P<perc>[\d\.]+)%%\])?   # percentage (optional)
            \s*                          # skip
            (?P<rest>.*)$                # lead-out
        """ % ored_keys
        perf_pat = re.compile (perf_patstr, re.VERBOSE)
    
        sample   = dict() 
        last_ts  = None
        ts       = None

        # and go
        for line in perf_out :
    
            l = ru.ReString (line)
    
          # print "line: %s" % line
    
            while l // (perf_pat) :
    
                ts   =     float(l.get ('time'))
                key  = perf_keys[l.get ('key')]
                val  =           l.get ('val')
                perc =           l.get ('perc')
    
                if  not perc :
                    perc = '-1.0'
    
              # print " ->  %s/%s  %s  %s  %s" % (ts, last_ts, key, val, perc)
    
                if ts != last_ts:
                    if last_ts != None:
                      # print "append %s" % last_ts
                        self._data['cpu']['sequence'].append ([last_ts, sample])
                        sample = dict()
                    last_ts = ts
    
                sample[key] = float(val.replace  (',', ''))
                if perc != None:
                    sample['%s_perc' % key] = float(perc.replace  (',', ''))
    
              # print "rest: %s" % l.get ('rest')
                l = ru.ReString (l.get ('rest'))
    
        if ts and sample:
          # print "append %s" % ts
            self._data['cpu']['sequence'].append ([ts, sample])
    
    
# ------------------------------------------------------------------------------
    
