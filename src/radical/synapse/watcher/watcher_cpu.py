
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2015, RADICAL@Rutgers"
__license__   = "MIT"

import re
import os
import signal
import threading

import subprocess    as sp
import radical.utils as ru
import watcher_base  as wb


# ------------------------------------------------------------------------------
# 
def _parse_perf_total (perf_out) :

    info = dict()

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

            info['%s'      % key] = float(val.replace  (',', ''))
            info['%s_perc' % key] = float(perc.replace (',', ''))

          # print "rest: %s" % l.get ('rest')
            l = ru.ReString (l.get ('rest'))

    # must haves
    if not 'ops'                  in info : info['ops'                  ] = 1
    if not 'cycles_idle_front'    in info : info['cycles_idle_front'    ] = 0
    if not 'cycles_idle_back'     in info : info['cycles_idle_back'     ] = 0
    if not 'cycles_stalled_front' in info : info['cycles_stalled_front' ] = 0
    if not 'cycles_stalled_back'  in info : info['cycles_stalled_back'  ] = 0

    info['efficiency']  = info['ops']                       \
                          / ( info['ops']                   \
                            + info['cycles_stalled_front']  \
                            + info['cycles_stalled_back']   \
                            )

    # also determine the theoretical number of FLOPS, which is calculated as
    #   FLOPS = #cores * #cycles/sec * flops/cycle
    # where flops/cycle are assumed to be 4 (see wikipedia on FLOPS).  We assume
    # that the watched process uses only one core, so we calculate the number
    # for one core only, but also report the number of cores.

    return info



# ------------------------------------------------------------------------------
# 
def _parse_perf_sample (perf_out) :

    # --------------------------------------------------------------------------
    def _handle_event(event):
        # must haves
        if event.get('ops'                 ) : event['ops'                  ] = 1
        if event.get('cycles_stalled_front') : event['cycles_stalled_front' ] = 0
        if event.get('cycles_stalled_back' ) : event['cycles_stalled_back'  ] = 0

        event['efficiency']  = event['ops']                       \
                               / ( event['ops']                   \
                                 + event['cycles_stalled_front']  \
                                 + event['cycles_stalled_back']   \
                                 )
        return event

    # --------------------------------------------------------------------------
    info = dict()

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
        (?P<time>\d\.\d+)            # timestamp
        \s+                          # skip
        (?P<val>[\d\.,]+)%%?         # value
        \s+                          # skip
        (?P<key>%s)                  # key
        \s*                          # skip
        (\[(?P<perc>[\d\.]+)%%\])?   # percentage (optional)
        \s*                          # skip
        (?P<rest>.*)$                # lead-out
    """ % ored_keys
    perf_pat = re.compile (perf_patstr, re.VERBOSE)

    sequence = list()
    event    = dict() 
    last_ts  = None
    ts       = None

    # and go
    for line in perf_out :

        l = ru.ReString (line)

        print "line: %s" % line

        while l // (perf_pat) :

            ts   =           l.get ('time')
            key  = perf_keys[l.get ('key')]
            val  =           l.get ('val')
            perc =           l.get ('perc', '-1.0')

            if  not perc :
                perc = '-1.0'

            print " ->  %s  %s  %s  %s" % (time, key, val, perc)

            info['%s'      % key] = float(val.replace  (',', ''))
            info['%s_perc' % key] = float(perc.replace (',', ''))

            if ts != last_ts:
                if ts:
                    sequence.append ([last_ts, _handle_event(event)])
                    last_ts = ts
                    event   = dict()

            event[key] = val

          # print "rest: %s" % l.get ('rest')
            l = ru.ReString (l.get ('rest'))

    if ts and event:
        sequence.append([ts, _handle_event(event)])

    info['sequence'] = sequence

    return info



# ------------------------------------------------------------------------------
#
class WatcherCPU (wb.WatcherBase) :

    # --------------------------------------------------------------------------
    #
    def __init__ (self, pid):

        wb.WatcherBase.__init__(self, pid)


    # --------------------------------------------------------------------------
    #
    # FIXME: for some reasons, running w/o shell=True fails.   So we need to
    # take a detour to communicate the perf pid.  We should try to get rid of
    # the shelling...
    #
    def _pre_process (self, config):

        rate = config.get ('sample_rate', 1) # sample rate in seconds
        rate = rate * 1000                   # perf wants milliseconds

        self._data['cpu'] = dict()

        sample_cmd  = "sh -c 'perf stat -I %d -p %d & PID=$!; " % (rate, self._pid) \
                    + "echo $PID > /tmp/synapse.pid.cpu_sample.$PPID; " \
                    + "wait $PID'" 
        print sample_cmd
        self._psam  = sp.Popen (sample_cmd,
                                stdout = sp.PIPE,
                                stderr = sp.STDOUT,
                                shell  = True)
        total_cmd   = "sh -c 'perf stat -v -p %d & PID=$!; " % (self._pid) \
                    + "echo $PID > /tmp/synapse.pid.cpu_total.$PPID; " \
                    + "wait $PID'" 
        print total_cmd
        self._ptot  = sp.Popen (total_cmd,
                                stdout = sp.PIPE,
                                stderr = sp.STDOUT,
                                shell  = True)


    # --------------------------------------------------------------------------
    #
    def _post_process (self):

        try:

            # proc should be done now -- let it know.  But first make sure we are
            # listening on the pipes when it dies...
            print      '/tmp/synapse.pid.cpu_total.%s' % self._ptot.pid
            perf_pid = int(open ('/tmp/synapse.pid.cpu_total.%s' % self._ptot.pid, 'r').read().strip())
            os.unlink ('/tmp/synapse.pid.cpu_total.%s' % self._ptot.pid)

            threading.Timer (1.0, os.kill, [perf_pid, signal.SIGINT]).start ()
            out = self._ptot.communicate()[0]

            ru.dict_merge (self._data['cpu'], _parse_perf_total (out))


            # now do the same for the sampling counters
            print      '/tmp/synapse.pid.cpu_sample.%s' % self._psam.pid
            perf_pid = int(open ('/tmp/synapse.pid.cpu_sample.%s' % self._psam.pid, 'r').read().strip())
            os.unlink ('/tmp/synapse.pid.cpu_sample.%s' % self._psam.pid)

            threading.Timer (1.0, os.kill, [perf_pid, signal.SIGINT]).start ()
            out = self._psam.communicate()[0]

            ru.dict_merge (self._data['cpu'], _parse_perf_sample (out))


          # cycles_used = self._data['ops'] / self._data['flops_per_cycle']
          # cycles_max  = self._data['frequency'] * self._data]['real']
          # if cycles_max :
          #     self._data['utilization'] = cycles_used / cycles_max
          # else:
          #     self._data['utilization'] = 0.0


        except Exception as e:

            print "Exception in postprocess: %s" % e



# ------------------------------------------------------------------------------

