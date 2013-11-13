
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
def benchmark_function (f, *args, **kwargs) :

    def func_wrapper (f, q, *args, **kwargs) :


        start_io  = get_io_usage  ()
        start_mem = get_mem_usage ()

        # wait for startup signal
        _ = q.get ()

        # do the deed
        ret = f ()


        end_io  = get_io_usage  ()
        end_mem = get_mem_usage ()

        info = dict()

        for key in end_io  :
            s_start   = start_io[key]
            s_end     = end_io  [key]
            n_start   = human_to_number (s_start)
            n_end     = human_to_number (s_end)
            info[key] = n_end-n_start

        for key in end_mem :
            s_start   = start_mem[key]
            s_end     = end_mem  [key]
            n_start   = human_to_number (s_start)
            n_end     = human_to_number (s_end)
            info[key] = n_end-n_start

        # send stop signal
        q.put (info)

    # use a queue to sync with the multi-subprocess
    q = mp.Queue ()

    # run the func in a separate process, but wrap into the wrapper
    p = mp.Process (target=func_wrapper, args=(f, q, args, kwargs))
    p.start ()

    # tell perf to watch the new process
    perf = sp.Popen ("/usr/bin/time -p perf stat -p %d" % p.pid,
                     stdout     = sp.PIPE,
                     stderr     = sp.PIPE,
                     shell      = True,
                     preexec_fn = os.setsid)


    _    = q.put (True) # tell the wrapper to do the deed...
    info = q.get ()     # ... and wait 'til the deed is done

    # perf should be done now -- let it know
    def killperf (pid) :
        os.killpg (pid, signal.SIGINT)

    t = threading.Timer (1.0, killperf, [perf.pid])
    t.start ()
    perf_out = perf.communicate()[1].split ('\n')

    for line in perf_out :

        l = ru.ReString (line)

        perf_keys = "instructions|branches|branch-misses|cycles|" \
                    "frontend cycles idle|backend  cycles idle|insns per cycle"

        while l // ('^.*?\s+(?P<val>[\d\.,]+)%%?\s+(?P<key>%s)(?P<rest>.*)' % perf_keys) :
            key = l.get ('key')
            val = l.get ('val')
            info['cpu.%s' % key] = val.replace (',', '')

            l = ru.ReString (l.get ('rest'))

        time_keys = "real|user|sys"

        while l // ('^(?P<key>%s)\s+(?P<val>[\d\.]+)' % time_keys) :
            key = l.get ('key')
            val = l.get ('val')
            info['time.%s' % key] = val.replace (',', '')

            l = ru.ReString (l.get ('rest'))


    return info




# ------------------------------------------------------------------------------

