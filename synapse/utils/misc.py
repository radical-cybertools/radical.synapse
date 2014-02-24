

import re
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

# import pudb 
# pudb.set_interrupt_handler ()

import synapse
import synapse.atoms   as sa

PROFILE_URL = '%s/synapse_profiles/' % synapse.SYNAPSE_DBURL
LOAD        = int (os.environ.get ('LOAD', '0'))
LOAD_CMD    = "top -b -n1 | head -1 | cut -f 5 -d : | cut -f 1 -d ," 

# ------------------------------------------------------------------------------
#
# see http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
#
def get_mem_usage () :

    info    = {'mem'     : dict()}
    scale   = {'kb'      : 1024.0,
               'mb'      : 1     }
    keymap  = {'VmPeak:' : 'peak',
               'VmSize:' : 'size',
               'VmData:' : 'data',
               'VmRSS:'  : 'resident',
               'VmStk:'  : 'stack'}

    with open ('/proc/%d/status'  %  os.getpid ()) as t :

        text = t.read ()

        for key in keymap.keys () :

            i = text.index (key)
            v = text[i:].split (None, 3)

            if  len(v) >= 2 :
                info['mem'][keymap[key]] = human_to_number (v[1])

        return info


# ------------------------------------------------------------------------------
#
def get_io_usage () :

    info   = {'io'           : dict()}
    keymap = {'read_bytes:'  : 'read' ,
              'write_bytes:' : 'write'}

    with open ('/proc/%d/io'  %  os.getpid ()) as t :

        text = t.read ()

        for key in keymap.keys () :

            i = text.index (key)
            v = text[i:].split (None, 3)

            if  len(v) >= 2 :
                info['io'][keymap[key]] = "%d" % int(v[1])

        return info


# ------------------------------------------------------------------------------
#
#
PREFIX_BIN = { 'K' : 1024,
               'M' : 1024 * 1024,
               'G' : 1024 * 1024 * 1024,
               'T' : 1024 * 1024 * 1024 * 1024,
               'P' : 1024 * 1024 * 1024 * 1024 * 1024,
               'E' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024,
               'Z' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024,
               'Y' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
             }

PREFIX_ISO = { 'K' : 1000,
               'M' : 1000 * 1000,
               'G' : 1000 * 1000 * 1000,
               'T' : 1000 * 1000 * 1000 * 1000,
               'P' : 1000 * 1000 * 1000 * 1000 * 1000,
               'E' : 1000 * 1000 * 1000 * 1000 * 1000 * 1000,
               'Z' : 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000,
               'Y' : 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
             }


# ------------------------------------------------------------------------------
#
def human_to_number (h, prefix=PREFIX_BIN) :

    rs = ru.ReString (h)

    with rs // '^\s*([\d\.]+)\s*(\D+)\s*$' as match : 
        if  not match :
          # print 'incorrect format: %s' % h
            return float(h)

        p = match[1].upper()[0]

        if  not p in prefix :
          # print 'unknown prefix: %s' % h
            return float(h)

        return float(match[0]) * prefix[p]


# ------------------------------------------------------------------------------
#
def number_to_human (n, prefix=PREFIX_BIN, unit='', template="%(val)f %(unit)s") :

    for key in prefix.keys () :

        hn = n / float(prefix[key])
        if  hn > 1 and hn < 1000 :
            return template % {'val' : hn, 'unit' : "%s%s" % (key, unit)}

    return template % {'val' : n, 'unit' : unit}


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

        info = {'io'  : dict(), 
                'cpu' : dict(),
                'mem' : dict(), 
                'net' : dict(), 
                'sys' : dict()}

        start_io  = get_io_usage  ()

        # wait for startup signal
        _ = q.get ()

        # start stress, get it spinning for one min to et a confirmed load
        # measurement, then run our own load, then kill stress.
        if  LOAD > 0 :
            synapse._logger.info ("creating system load %s" % LOAD)
            os.popen ("killall -9 stress 2>&1 > /dev/null")
            os.popen ('stress --cpu %s&' % LOAD)
            time.sleep (60)

        time_1 = time.time()
        load_1 = float(os.popen (LOAD_CMD).read())

        # do the deed
        ret = func (*args, **kwargs)

        end_io  = get_io_usage  ()
        end_mem = get_mem_usage  ()

        for key in end_io['io']  :
            s_start   = start_io['io'][key]
            s_end     = end_io  ['io'][key]
            n_start   = human_to_number (s_start)
            n_end     = human_to_number (s_end)
            info['io'][key] = n_end-n_start

        for key in end_mem['mem']  :
            info['mem'][key] = human_to_number (end_mem['mem'][key])

        time_2 = time.time()
        load_2 = float(os.popen (LOAD_CMD).read())
        info['sys']['load'] = max(load_1, load_2)
        synapse._logger.info ("system load %s: %s" % (LOAD, info['sys']['load']))



        if  LOAD > 0 :
            synapse._logger.info ("stopping system load")
            os.popen ("killall -9 stress 2>&1 > /dev/null")
            synapse._logger.info ("stopped  system load")

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

  # pprint.pprint (info)
    ru.dict_merge (info, _parse_perf_output (out))
  # pprint.pprint (info)

    cycles_used = info['cpu']['ops'] / info['cpu']['flops_per_cycle']
    cycles_max  = info['cpu']['frequency'] * info['time']['real']
    info['cpu']['utilization'] = cycles_used / cycles_max

  # print "utilization    : %s \n" % info['cpu']['utilization']
  #
  # print "cycles_max     : %s " % cycles_max 
  # print "frequency      : %s " % info['cpu']['frequency']
  # print "time           : %s \n" % info['time']['real']
  #
  # print "cycles_used    : %s " % cycles_used
  # print "cycles         : %s " % info['cpu']['cycles']
  # print "stalled_front  : %s " % info['cpu']['cycles_stalled_front']
  # print "stalled_back   : %s " % info['cpu']['cycles_stalled_back']

    # don't return any stdout, thus the None
    return (info, ret, None)  


# ------------------------------------------------------------------------------
#
def profile_command (command) :

    info = {'io'  : dict(), 
            'cpu' : dict(),
            'mem' : dict(), 
            'net' : dict(), 
            'sys' : dict()}

    # start stress, get it spinning for one min to et a confirmed load
    # measurement, then run our own load, then kill stress.
    if  LOAD > 0 :
        synapse._logger.info ("creating system load %s" % LOAD)
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        os.Popen ('stress --cpu %s &' % LOAD)
        time.sleep (60)

    time_1 = time.time()
    load_1 = float(os.popen (LOAD_CMD).read())
    synapse._logger.info ("creating system load %s: %s" % (LOAD, info['sys']['load']))

    # run the profiled command in a separate process
    pcommand = "/usr/bin/time -v perf stat %s" % command
    args     = shlex.split (pcommand)
    proc     = sp.Popen    (args, shell=False, stdout=sp.PIPE, stderr=sp.STDOUT)
    out      = proc.communicate ()[0]
    ret      = proc.returncode

    time_2 = time.time()
    load_2 = float(os.popen (LOAD_CMD).read())
    info['sys']['load'] = max(load_1, load_2)
    synapse._logger.info ("system load %s: %s" % (LOAD, info['sys']['load']))

    if  LOAD > 0 :
        synapse._logger.info ("stopping system load")
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        synapse._logger.info ("stopped  system load")

  # pprint.pprint (info)
    ru.dict_merge (info, _parse_perf_output (out))
  # pprint.pprint (info)
 
    cycles_used = info['cpu']['ops'] / info['cpu']['flops_per_cycle']
    cycles_max  = info['cpu']['frequency'] * info['time']['real']
    info['cpu']['utilization'] = cycles_used / cycles_max

  # print "utilization    : %s \n" % info['cpu']['utilization']
  #
  # print "cycles_max     : %s " % cycles_max 
  # print "frequency      : %s " % info['cpu']['frequency']
  # print "time           : %s \n" % info['time']['real']
  #
  # print "cycles_used    : %s " % cycles_used
  # print "cycles         : %s " % info['cpu']['cycles']
  # print "stalled_front  : %s " % info['cpu']['cycles_stalled_front']
  # print "stalled_back   : %s " % info['cpu']['cycles_stalled_back']

    store_profile (command, info)

    return info, ret, out


# ------------------------------------------------------------------------------
#
def emulate_command (command) :

    profile    = get_profile (command)
    old_info   = profile['profiles'][0]

    flops      = int(old_info['cpu']['cycles'] / 8 / 1024 / 1024)
    efficiency = int(old_info['cpu']['efficiency'])
    mem        = int(old_info['mem']['max']        / 1024 / 1024)
  # io_in      = int(old_info['io']['in']) 
  # io_out     = int(old_info['io']['out'])
    io_in      = 0
    io_out     = 0

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

    new_info['cpu']['efficiency']  = new_info['cpu']['ops']                       \
                                     / ( new_info['cpu']['ops']                   \
                                       + new_info['cpu']['cycles_stalled_front']  \
                                       + new_info['cpu']['cycles_stalled_back']   \
                                       )
                                 
   #print 'efficiency = %s / (%s + %s + %s) = %s' % (
   #          new_info['cpu']['ops'],
   #          new_info['cpu']['ops'],
   #          new_info['cpu']['cycles_stalled_front'],
   #          new_info['cpu']['cycles_stalled_back'],
   #          new_info['cpu']['efficiency'])

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
    perf_pat    = re.compile (perf_patstr, re.VERBOSE)

    # and go
    for line in perf_out :

        synapse._logger.debug ("perf out: %s" % line)

        l = ru.ReString (line)

        while l // (perf_pat) :

            key  = perf_keys[l.get ('key')]
            val  =           l.get ('val')
            perc =           l.get ('perc', '-1.0')

            if  not perc :
                perc = '-1.0'

          # print " ->  %s  %s  %s" % (key, val, perc)

            info['cpu']['%s'      % key] = float(val.replace  (',', ''))
            info['cpu']['%s_perc' % key] = float(perc.replace (',', ''))

          # print "rest: %s" % l.get ('rest')
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
    if not 'ops'                  in info['cpu'] : info['cpu']['ops'                  ] = 1
    if not 'peak'                 in info['mem'] : info['mem']['peak'                 ] = 0
    if not 'max'                  in info['mem'] : info['mem']['max'                  ] = 0
    if not 'cycles_idle_front'    in info['cpu'] : info['cpu']['cycles_idle_front'    ] = 0
    if not 'cycles_idle_back'     in info['cpu'] : info['cpu']['cycles_idle_back'     ] = 0
    if not 'cycles_stalled_front' in info['cpu'] : info['cpu']['cycles_stalled_front' ] = 0
    if not 'cycles_stalled_back'  in info['cpu'] : info['cpu']['cycles_stalled_back'  ] = 0

    info['cpu']['efficiency']  = info['cpu']['ops']                       \
                                 / ( info['cpu']['ops']                   \
                                   + info['cpu']['cycles_stalled_front']  \
                                   + info['cpu']['cycles_stalled_back']   \
                                   )
                                 
  # print 'efficiency = %s / (%s + %s + %s) = %s' % (
  #           info['cpu']['ops'],
  #           info['cpu']['ops'],
  #           info['cpu']['cycles_stalled_front'],
  #           info['cpu']['cycles_stalled_back'],
  #           info['cpu']['efficiency'])

    # also determine the theoretical number of FLOPS, which is calculated as
    #   FLOPS = #cores * #cycles/sec * flops/cycle
    # where flops/cycle are assumed to be 4 (see wikipedia on FLOPS).  We assume
    # that the watched process uses only one core, so we calculate the number
    # for one core only, but also report the number of cores.
    with open ("/proc/cpuinfo") as proc_cpuinfo:

        cpu_freq         = 1 # in Hz
        num_sockets      = 1
        cores_per_socket = 1 
        core_siblings    = 1
        threads_per_core = 1
        flops_per_cycle  = 4 # see wikipedia on FLOPS
        flops_per_core   = flops_per_cycle * cpu_freq

        for line in proc_cpuinfo.readlines ()  :

            if  line.startswith ('model name') :
                elems = line.split ('@')
                if  elems[-1].endswith ('Hz\n') :
                    cpu_freq = max(cpu_freq, human_to_number (elems[-1], prefix=PREFIX_ISO))

            if  line.startswith ('cpu MHz') :
                elems = line.split (':')
                cpu_freq = max(cpu_freq, float(elems[-1]) * 1000*1000)

            if  line.startswith ('physical id') :
                elems = line.split (':')
                num_sockets = max(num_sockets, int(elems[-1])+1)

            if  line.startswith ('cpu cores') :
                elems = line.split (':')
                cores_per_socket = max(cores_per_socket, int(elems[-1]))

            if  line.startswith ('siblings') :
                elems = line.split (':')
                core_siblings = max(core_siblings, int(elems[-1]))

        threads_per_core = int(core_siblings / cores_per_socket)
        flops_per_core   = int(cpu_freq * flops_per_cycle)

  # print "cpu_freq         : %d" % cpu_freq         
  # print "num_sockets      : %d" % num_sockets      
  # print "cores_per_socket : %d" % cores_per_socket 
  # print "core_siblings    : %d" % core_siblings    
  # print "threads_per_core : %d" % threads_per_core 
  # print "flops_per_cycle  : %d" % flops_per_cycle  
  # print "flops_per_core   : %d" % flops_per_core   

    info['cpu']['frequency'        ] = cpu_freq         
    info['cpu']['num_sockets'      ] = num_sockets      
    info['cpu']['cores_per_socket' ] = cores_per_socket 
    info['cpu']['threads_per_core' ] = threads_per_core 
    info['cpu']['flops_per_cycle'  ] = flops_per_cycle  
    info['cpu']['flops_per_core'   ] = flops_per_core   

    time_cutoff = float(1.0 / 1000 / 1000)
    stime = info['time']['system']
    if  float(stime) < time_cutoff :
        stime = max(time_cutoff, info['time']['real'])
        
  # pprint.pprint (info)

    return info


# ------------------------------------------------------------------------------
def store_profile (command, info) :

    command_idx = index_command (command)

    host, port, dbname, _, _ = ru.split_dburl (PROFILE_URL)

  # print 'url       : %s' % PROFILE_URL
  # print 'host      : %s' % host
  # print 'port      : %s' % port
  # print 'database  : %s' % dbname

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]
    collection = database['profiles']

    profile    = {'type'     : 'profile', 
                  'command'  : command, 
                  'index'    : command_idx, 
                  'profiles' : list()}
    results    = collection.find ({'type'  : 'profile', 
                                   'index' : command_idx})

    if  results.count() :
        # expand existing profile
        profile = results[0]


    profile['profiles'].append (info)

    collection.save (profile)
  # print 'profile stored in %s' % [host, port, dbname, 'profiles']


# ------------------------------------------------------------------------------
def get_profile (command) :

    command_idx = index_command (command)

    host, port, dbname, _, _ = ru.split_dburl (PROFILE_URL)

  # print 'url       : %s' % PROFILE_URL
  # print 'host      : %s' % host
  # print 'port      : %s' % port
  # print 'database  : %s' % dbname

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]
    collection = database['profiles']

    results    = collection.find ({'type'    : 'profile', 
                                   'command' : command,
                                   'index'   : command_idx})

    if  not results.count() :
        raise RuntimeError ("Could not get profile for %s at %s/profiles" % (command, PROFILE_URL))


  # print 'profile retrieved from %s' % [host, port, dbname, 'profiles']
  # pprint.pprint (results[0])
    return results[0]


# ------------------------------------------------------------------------------
#
def index_command (command) :
    """remove hosts from URLs for cross-site indexing"""

    ret = "%s" % command # deep copy

    if  '://' in command :
        url_idx   = command.find ('://')
        host_idx  = command.find ('/', url_idx+3)
      # print '----'
      # print command
      # print url_idx
      # print host_idx
      # print command[:url_idx]
      # print command[host_idx:]
        ret   = "%s:/%s" % (command[:url_idx], command[host_idx:])
      # print ret
      # print '----'

    return ret


# ------------------------------------------------------------------------------

