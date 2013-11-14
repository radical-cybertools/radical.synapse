
# see http://stackoverflow.com/questions/938733/total-memory-used-by-python-process

import os
import time
import threading
import signal
import radical.utils   as ru
import subprocess      as sp
import multiprocessing as mp


# ------------------------------------------------------------------------------
#
def get_mem_usage () :

    ret   = dict ()

    scale = {'kb'      : 1024.0,
             'mb'      : 1     }
    info  = {'VmPeak:' : 'mem.peak',
             'VmSize:' : 'mem.size',
             'VmData:' : 'mem.data',
             'VmRSS:'  : 'mem.resident',
             'VmStk:'  : 'mem.stack'}

    with open ('/proc/%d/status'  %  os.getpid ()) as t :

        text = t.read ()

        for key in info.keys () :

            i = text.index (key)
            v = text[i:].split (None, 3)

            if  len(v) < 3 :
                ret[info[key]] = -1
            else :
                ret[info[key]] = "%f MB" % (float(v[1]) / scale[v[2].lower ()])

        return ret


# ------------------------------------------------------------------------------
#
def get_io_usage () :

    ret   = dict ()
    info  = {'read_bytes:'  : 'io.read' ,
             'write_bytes:' : 'io.write'}

    with open ('/proc/%d/io'  %  os.getpid ()) as t :

        text = t.read ()

        for key in info.keys () :

            i = text.index (key)
            v = text[i:].split (None, 3)

            if  len(v) < 2 :
                ret[info[key]] = -1
            else :
                ret[info[key]] = "%d" % int(v[1])

        return ret


# ------------------------------------------------------------------------------
#
#
PREFIX = { 'k' : 1024,
           'm' : 1024 * 1024,
           'g' : 1024 * 1024 * 1024,
           't' : 1024 * 1024 * 1024 * 1024,
           'p' : 1024 * 1024 * 1024 * 1024 * 1024,
           'e' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024,
           'z' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024,
           'y' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
         }


# ------------------------------------------------------------------------------
#
def human_to_number (h) :

    rs = ru.ReString (h)

    with rs // '^\s*([\d\.]+)\s*(\D+)\s*$' as match : 
        if  not match :
         #  print 'incorrect format: %s' % h
            return float(h)

        p = match[1].lower()[0]

        if  not p in PREFIX :
         #  print 'unknown prefix: %s' % h
            return float(h)

        return float(match[0]) * PREFIX[p]


# ------------------------------------------------------------------------------
#
def time_to_seconds (t) :

    rs = ru.ReString (t)

    with rs // '^(?:\s*(\d+)\s*[:])+\s*([\d\.]+)\s*$' as match :

        if  not match :
            return t

        seconds = 0
        if  len(match) ==  1 : seconds = float(match[0])
        if  len(match) ==  2 : seconds = float(match[0]) * 60      + float(match[1])
        if  len(match) ==  3 : seconds = float(match[0]) * 60 * 60 + float(match[1]) * 60 + float(match[2])

        return seconds




# ------------------------------------------------------------------------------
#
def benchmark_function (f, *args, **kwargs) :

    def func_wrapper (f, q, args, kwargs) :

        start_io  = get_io_usage  ()

        # wait for startup signal
        _ = q.get ()

        # do the deed
        ret = f (*args, **kwargs)

        end_io  = get_io_usage  ()
        end_mem = get_mem_usage  ()

        info = dict()

        for key in end_io  :
            s_start   = start_io[key]
            s_end     = end_io  [key]
            n_start   = human_to_number (s_start)
            n_end     = human_to_number (s_end)
            info[key] = n_end-n_start

        for key in end_mem  :
            info[key] = human_to_number (end_mem [key])

        # send stop signal
        q.put (ret)
        q.put (info)

    # use a queue to sync with the multi-subprocess
    q = mp.Queue ()

    # run the func in a separate process, but wrap into the wrapper
    p = mp.Process (target = func_wrapper, 
                    args   = (f, q), 
                    kwargs = {'args'   : args, 
                              'kwargs' : kwargs})
    p.start ()

    # tell perf to watch the new process
    perf = sp.Popen ("/bin/sh -c '/usr/bin/time -v perf stat -p %d'" % p.pid,
                     stdout     = sp.PIPE,
                     stderr     = sp.STDOUT,
                     shell      = True,
                     preexec_fn = os.setsid)


    _    = q.put (True) # tell the wrapper to do the deed...
    ret  = q.get ()     # ... and wait 'til the deed is done
    info = q.get ()     # ... and get statistics
    time.sleep  (1)     # make sure the procs are done

    # perf should be done now -- let it know.  But first make sure we are
    # listening on the pipes when it dies...
    def killperf (pid) :
        try :
            os.killpg (pid, signal.SIGINT)
        except :
            pass

    threading.Timer (2.0, killperf, [perf.pid]).start ()
    perf_out = perf.communicate()[0].split ('\n')


    for line in perf_out :

        l = ru.ReString (line)

        perf_keys = {"instructions"         : "cpu.ops",
                     "branches"             : "cpu.branches",
                     "branch-misses"        : "cpu.branch_misses",
                     "cycles"               : "cpu.cycles",
                     "frontend cycles idle" : "cpu.cycles idle front",
                     "backend  cycles idle" : "cpu.cycles idle back",
                     "insns per cycle"      : "cpu.ops/cycle"}

        while l // ( '^.*?\s+(?P<val>[\d\.,]+)%%?\s+(?P<key>%s)(?P<rest>.*)' \
                   % '|'.join(perf_keys.keys())) :
            key = perf_keys[l.get ('key')]
            val =           l.get ('val')
            info['%s' % key] = float(val.replace (',', ''))

            l = ru.ReString (l.get ('rest'))

        l = ru.ReString (line)
        if l // '^\s*User time \(.*?\):\s+([\d\.]+)\s*$' :
            info["time.user"] = float(l.get ()[0].replace(',', ''))
        if l // '^\s*System time \(.*?\):\s+([\d\.]+)\s*$' :
            info["time.system"] = float(l.get ()[0].replace(',', ''))
        if l // '^\s*Elapsed \(.*?\).*?\(.*?\):\s+([\d\.:]+)\s*$' :
            info["time.real"] = float(time_to_seconds (l.get ()[0].replace(',', '')))
        if l // '^\s*Maximum resident set .*?\(.*?\):\s+([\d\.]+)\s*$' :
            info["mem.max"] = int(l.get ()[0].replace(',', ''))*1024
        if l // '^\s*Exit status:\s+([\d\.]+)\s*$' :
            info["sys.exit"] = int(l.get ()[0].replace(',', ''))


        # must haves
        if not 'cpu.ops'              in info : info['cpu.ops'              ] = 0
        if not 'mem.peak'             in info : info['mem.peak'             ] = 0
        if not 'mem.max'              in info : info['mem.max'              ] = 0
        if not 'cpu.cycles idle front'in info : info['cpu.cycles idle front'] = 0
        if not 'cpu.cycles idle back' in info : info['cpu.cycles idle back' ] = 0

    return ret, info




# ------------------------------------------------------------------------------

