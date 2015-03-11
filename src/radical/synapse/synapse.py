

import os
import time
import pprint
import threading
import radical.utils   as ru
import subprocess      as sp
import multiprocessing as mp

import watcher as rsw
import utils   as rsu
import atoms   as rsa

# import pudb 
# pudb.set_interrupt_handler ()


# ------------------------------------------------------------------------------
#
_LOAD     = int (os.environ.get ('LOAD', '0'))
_LOAD_CMD = "top -b -n1 | head -1  |       cut -f 4 -d :         | cut -f 1 -d ,"
_LOAD_CMD = "top -b -n1 | head -n1 | rev | cut -f 3 -d \  | rev  | sed -e 's/,//'"


# ------------------------------------------------------------------------------
#
def profile_function (func, *args, **kwargs) :

    # --------------------------------------------------------------------------
    def func_wrapper (func, q, args, kwargs) :

        info = dict()

        start_io  = get_io_usage  ()
      # pprint.pprint (start_io)

        # wait for startup signal
        _ = q.get ()

        # start stress, get it spinning for one min to et a confirmed load
        # measurement, then run our own load, then kill stress.
        if  _LOAD > 0 :
            rsu.logger.info ("creating system load %d" % _LOAD)
            os.popen ("killall -9 stress 2>&1 > /dev/null")
            os.popen ('stress --cpu %d &' % _LOAD)
            time.sleep (60)

        rsu.logger.info ("system load cmd: %s" % (_LOAD_CMD))
        load_1  = float(os.popen (_LOAD_CMD).read())
        time_1  = rsu.timestamp()

        # do the deed
        ret = func (*args, **kwargs)

        time_2  = rsu.timestamp()
        end_io  = get_io_usage  ()
        end_mem = get_mem_usage  ()

      # pprint.pprint (end_io)

        for key in end_io['io']  :
            s_start   = start_io['io'][key]
            s_end     = end_io  ['io'][key]
            n_start   = human_to_number (s_start)
            n_end     = human_to_number (s_end)
            info['io'][key] = n_end-n_start

        for key in end_mem['mem']  :
            info['mem'][key] = human_to_number (end_mem['mem'][key])

        time_2 = rsu.timestamp()
        load_2 = float(os.popen (_LOAD_CMD).read())
        info['cpu']['load'] = max(load_1, load_2)
        rsu.logger.info ("system load %s: %s" % (_LOAD, info['cpu']['load']))
        rsu.logger.info ("app mem     %s: %s" % (_LOAD, info['mem']))

        info['time']['start'] = rsu.time_zero()
        info['time']['real']  = time_2 - time_1


        if  _LOAD > 0 :
            rsu.logger.info ("stopping system load")
            os.popen ("killall -9 stress 2>&1 > /dev/null")
            rsu.logger.info ("stopped  system load")

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

    # do we have perf?
    if  'no perf in' in sp.Popen ("which perf", 
                                  shell=True,
                                  stdout=sp.PIPE, 
                                  stderr=sp.STDOUT).stdout.read () :
        prof = None

    else :
        # profile the new process
        # FIXME: this will miss the process startup...
        prof = sp.Popen ("/bin/sh -c '/usr/bin/time -v perf stat -p %d'" % (proc.pid),
                         stdout     = sp.PIPE,
                         stderr     = sp.STDOUT,
                         shell      = True,
                         preexec_fn = os.setsid)



    _    = q.put (True) # tell the wrapper to do the deed...
    ret  = q.get ()     # ... and wait 'til the deed is done
    info = q.get ()     # ... and get statistics
    time.sleep  (1)     # make sure the procs are done


    if  prof :

        # prof should be done now -- let it know.  But first make sure we are
        # listening on the pipes when it dies...
        threading.Timer (2.0, _killproc, [prof.pid]).start ()
        out = prof.communicate()[0]

      # pprint.pprint (info)
      # pprint.pprint (_parse_perf_output (out))
        ru.dict_merge (info, _parse_perf_output (out), policy='overwrite')
      # print '~~~~~~~~~~~~~~~~~~'
      # pprint.pprint (info)
      # print '~~~~~~~~~~~~~~~~~~'


        cycles_used = info['cpu']['ops'] / info['cpu']['flops_per_cycle']
        cycles_max  = info['cpu']['frequency'] * info['time']['real']

        cycles_max = max (1, cycles_max) # make sure its nonzero...

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


    if isinstance (command, list):
        command = ' '.join (command)

    info = {'cmd' : command}

    print "profile: %s" % command

    # start stress, get it spinning for one min to et a confirmed load
    # measurement, then run our own load, then kill stress.
    if  _LOAD > 0 :
        rsu.logger.info ("creating system load %s" % _LOAD)
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        os.popen ('stress --cpu %s &' % _LOAD)
        time.sleep (60)

    time_1 = rsu.timestamp()
    load_1 = float(os.popen (_LOAD_CMD).read())

  # pprint.pprint (info)
  # rsu.logger.info ("creating system load %s: %s" % (_LOAD, info['cpu']['load']))

  # # perf stat does not report pid -- so we do it... :/
  # command = "/bin/sh -c '%s & pid=$!; wait $pid; echo \"	PID: $pid\"'" % command

  # # wrap the command into perf stat
  # command = "perf stat %s" % command

  # # we also use 'time -v', so wrap once moe
  # command = "/usr/bin/time -v %s" % command

    print command
    start = rsu.timestamp()

    # run the profiled command in a separate process
    cmd = sp.Popen (command.split(), 
                    stdout = sp.PIPE,
                    stderr = sp.STDOUT)

    watchers = list()
    watchers.append (rsw.WatcherCPU (cmd.pid))
    watchers.append (rsw.WatcherIO  (cmd.pid))
    watchers.append (rsw.WatcherMem (cmd.pid))
    watchers.append (rsw.WatcherSys (cmd.pid))

    out = cmd.communicate ()[0]
    ret = cmd.returncode

    stop = rsu.timestamp()

    info['time'] = dict()
    info['time']['start'] = rsu.time_zero()
    info['time']['real']  = stop-start

    for watcher in reversed(watchers) :
        watcher.stop ()
        watcher.join ()
        ru.dict_merge (info, watcher.get_data())


    time_2 = rsu.timestamp()
    load_2 = float(os.popen (_LOAD_CMD).read())
    info['cpu']['load'] = max(load_1, load_2)
    rsu.logger.info ("system load %s: %s" % (_LOAD, info['cpu']['load']))

    if  _LOAD > 0 :
        rsu.logger.info ("stopping system load")
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        rsu.logger.info ("stopped  system load")

    cycles_used = info['cpu']['ops'] / info['cpu']['flops_per_cycle']
    cycles_max  = info['cpu']['frequency'] * info['time']['real']
    if cycles_max :
        info['cpu']['utilization'] = cycles_used / cycles_max
    else:
        info['cpu']['utilization'] = 0.0

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

    rsu.store_profile (command, info)

    return info, ret, out


# ------------------------------------------------------------------------------
#
def emulate_command (command) :

    profile    = get_profile (command)
    old_info   = profile['profiles'][0]

    flops      = int(old_info['cpu']['cycles'] / 8 / 1024 / 1024)
    efficiency = int(old_info['cpu']['efficiency'])
    mem        = int(old_info['mem']['max']        / 1024 / 1024)
    io_in      = int(old_info['i_o']['in']) 
    io_out     = int(old_info['i_o']['out'])
  # io_in      = 0
  # io_out     = 0

    def emulator (flops, mem, io_in, io_out) :

        app_c = rsa.Compute ()
        app_m = rsa.Memory  ()
        app_s = rsa.Storage ()
     #  app_n = rsa.Network ()

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

