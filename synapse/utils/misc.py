

import os
import time
import shlex
import signal
import pprint
import pymongo
import threading
import radical.utils   as ru
import subprocess      as sp
import multiprocessing as mp

import synapse
import synapse.atoms   as sa

PROFILE_URL = '%s/synapse_profiles/' % synapse.SYNAPSE_DBURL

# ------------------------------------------------------------------------------
#
# see http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
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
def profile_function (func, *args, **kwargs) :

    # --------------------------------------------------------------------------
    def func_wrapper (func, q, args, kwargs) :

        start_io  = get_io_usage  ()

        # wait for startup signal
        _ = q.get ()

        # do the deed
        ret = func (*args, **kwargs)

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
    # --------------------------------------------------------------------------



    # use a queue to sync with the multi-subprocess
    q = mp.Queue ()

    # run the func in a separate process, but wrap into the wrapper
    proc = mp.Process (target = func_wrapper, 
                       args   = (func, q), 
                       kwargs = {'args'   : args, 
                                 'kwargs' : kwargs})
    proc.start ()

    # tell perf to watch the new process
    perf = sp.Popen ("/bin/sh -c '/usr/bin/time -v perf stat -p %d'" % proc.pid,
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
    out = perf.communicate()[0]

    info.update (_parse_perf_output (out))


    # don't return any stdout, thus the None
    return (info, ret, None)  


# ------------------------------------------------------------------------------
#
def profile_command (command) :

    info = dict()

    # run the profiled command in a separate process
    pcommand = "/usr/bin/time -v perf stat %s" % command
    args     = shlex.split (pcommand)
    proc     = sp.Popen    (args, shell=False, stdout=sp.PIPE, stderr=sp.STDOUT)
    out      = proc.communicate ()[0]
    ret      = proc.returncode

    info.update (_parse_perf_output (out))

  # pprint.pprint (info)

    store_profile (command, info)

    return info, ret, out


# ------------------------------------------------------------------------------
#
def emulate_command (command) :

    profile  = get_profile (command)
    old_info = profile['profiles'][0]

    flops  = int(old_info['cpu']['cycles'] / 8 / 1024 / 1024)
    mem    = int(old_info['mem']['max']        / 1024 / 1024)
  # io_in  = int(old_info['io']['in']) 
  # io_out = int(old_info['io']['out'])
    io_in  = 0
    io_out = 0

    def emulator (flops, mem, io_in, io_out) :

        app_c = sa.Compute ()
        app_m = sa.Memory  ()
        app_s = sa.Storage ()
     #  app_n = sa.Network ()

        # the atoms below are executed concurrently (in their own threads)
        app_c.run (info={'n'   : flops})   # consume  10 GFlop CPY Cycles
        app_m.run (info={'n'   : mem})     # allocate  5 GByte memory
        app_s.run (info={'n'   : io_out,   # write     2 GByte to disk
                         'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})
     #  app_n.run (info={'type'   : 'server', # communicate a 1 MByte message
     #                   'mode'   : 'read',
     #                   'port'   : 10000,
     #                   'n'      : 100})
     #  time.sleep (1)
     #  app_n.run (info={'type'   : 'client',
     #                   'mode'   : 'write',
     #                   'host'   : 'localhost',
     #                   'port'   : 10000,
     #                   'n'      : 100})

      # # all are started -- now wait for completion and collect times
      # time_c = 0.0
      # time_m = 0.0
      # time_s = 0.0
     ## time_n = 0.0

        info_c = app_c.wait ()
        info_m = app_m.wait ()
        info_s = app_s.wait ()
     #  info_n = app_n.wait ()

      # time_c = float(info_c['timer'])
      # time_m = float(info_m['timer'])
      # time_s = float(info_s['timer'])
     ## time_n = float(info_n['timer'])

      # host   = os.getenv ('HOST', os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ())
      # output = '%-10s %10s ------- %7.2f %7.2f %7.2f %5d %5d %5d %5d' % \
      #         (host, "", time_c, time_m, time_s,
      #          0, flops, mem, io_out)

      # print output
      # f.write ("%s\n" % output)


    new_info, ret, _ = profile_function (emulator, flops, mem, io_in, io_out)

    return (new_info, ret, None)


# ------------------------------------------------------------------------------

def _parse_perf_output (perf_out) :

    info         = dict()
    info['cpu']  = dict()
    info['mem']  = dict()
    info['net']  = dict()
    info['sys']  = dict()
    info['time'] = dict()

    if  isinstance (perf_out, basestring) :
        perf_out = perf_out.split ('\n')

    for line in perf_out :

        l = ru.ReString (line)

        perf_keys = {"instructions"         : "ops",
                     "branches"             : "branches",
                     "branch-misses"        : "branch_misses",
                     "cycles"               : "cycles",
                     "frontend cycles idle" : "cycles idle front",
                     "backend  cycles idle" : "cycles idle back",
                     "insns per cycle"      : "ops/cycle"}

        while l // ( '^.*?\s+(?P<val>[\d\.,]+)%%?\s+(?P<key>%s)(?P<rest>.*)' \
                   % '|'.join(perf_keys.keys())) :
            key = perf_keys[l.get ('key')]
            val =           l.get ('val')
            info['cpu']['%s' % key] = float(val.replace (',', ''))

            l = ru.ReString (l.get ('rest'))

        l = ru.ReString (line)
        if  l // '^\s*User time \(.*?\):\s+([\d\.]+)\s*$' :
            info["time"]["user"] = float(l.get ()[0].replace(',', ''))
        if  l // '^\s*System time \(.*?\):\s+([\d\.]+)\s*$' :
            info["time"]["system"] = float(l.get ()[0].replace(',', ''))
        if  l // '^\s*Elapsed \(.*?\).*?\(.*?\):\s+([\d\.:]+)\s*$' :
            info["time"]["real"] = float(time_to_seconds (l.get ()[0].replace(',', '')))
        if  l // '^\s*Maximum resident set .*?\(.*?\):\s+([\d\.]+)\s*$' :
            info["mem"]["max"] = int(l.get ()[0].replace(',', ''))*1024
        if  l // '^\s*Exit status:\s+([\d\.]+)\s*$' :
            info["sys"]["exit"] = int(l.get ()[0].replace(',', ''))


    # must haves
    if not 'ops'              in info['cpu'] : info['cpu']['ops'              ] = 0
    if not 'peak'             in info['mem'] : info['mem']['peak'             ] = 0
    if not 'max'              in info['mem'] : info['mem']['max'              ] = 0
    if not 'cycles idle front'in info['cpu'] : info['cpu']['cycles idle front'] = 0
    if not 'cycles idle back' in info['cpu'] : info['cpu']['cycles idle back' ] = 0

    return info


# ------------------------------------------------------------------------------
def store_profile (command, info) :

    host, port, dbname, _, _ = split_dburl (PROFILE_URL)

  # print 'url       : %s' % PROFILE_URL
  # print 'host      : %s' % host
  # print 'port      : %s' % port
  # print 'database  : %s' % dbname

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]
    collection = database['profiles']

    profile    = {'type'     : 'profile', 
                  'command'  : command, 
                  'profiles' : list()}
    results    = collection.find ({'type'    : 'profile', 
                                   'command' : command})

    if  results.count() :
        # expand existing profile
        profile = results[0]


    profile['profiles'].append (info)

    collection.save (profile)
    print 'profile stored in %s' % [host, port, dbname, 'profiles']


# ------------------------------------------------------------------------------
def get_profile (command) :

    host, port, dbname, _, _ = split_dburl (PROFILE_URL)

  # print 'url       : %s' % PROFILE_URL
  # print 'host      : %s' % host
  # print 'port      : %s' % port
  # print 'database  : %s' % dbname

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]
    collection = database['profiles']

    results    = collection.find ({'type'    : 'profile', 
                                   'command' : command})

    if  not results.count() :
        # oops...
        return None

    print 'profile retrieved from %s' % [host, port, dbname, 'profiles']
  # pprint.pprint (results[0])
    return results[0]


# ------------------------------------------------------------------------------
#
def split_dburl (url) :
    """
    we split the url into the base mongodb URL, and the path element, whose
    first element is the database name, and the remainder is interpreted as
    collection id.
    """

    slashes = [idx for [idx,elem] in enumerate(url) if elem == '/']

    if  len(slashes) < 3 :
        raise ValueError ("url needs to be a mongodb URL, the path element " \
                          "must specify the database and collection id")

    if  url[:slashes[0]].lower() != 'mongodb:' :
        raise ValueError ("url must be a 'mongodb://' url, not %s" % url)

  # if  len(url) <= slashes[2]+1 :
  #     raise ValueError ("url needs to be a mongodb url, the path element " \
  #                       "must specify the database and collection id")

    base_url = url[slashes[1]+1:slashes[2]]
    path     = url[slashes[2]+1:]

    if  ':' in base_url :
        host, port = base_url.split (':', 1)
        port = int(port)
    else :
        host, port = base_url, None

    path = os.path.normpath(path)
    if  path.startswith ('/') :
        path = path[1:]
    path_elems = path.split ('/')


    dbname = None
    cname  = None
    pname  = None

    if  len(path_elems)  >  0 :
        dbname = path_elems[0]

    if  len(path_elems)  >  1 :
        dbname = path_elems[0]
        cname  = path_elems[1]

    if  len(path_elems)  >  2 :
        dbname = path_elems[0]
        cname  = path_elems[1]
        pname  = '/'.join (path_elems[2:])

    if  dbname == '.' : 
        dbname = None

    print str([host, port, dbname, cname, pname])
    return [host, port, dbname, cname, pname]


# ------------------------------------------------------------------------------

