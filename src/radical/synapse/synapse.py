

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
def profile (command, *args, **kwargs) :

    if callable (command):
        cmd_str = "%s %s %s" % (command.__name__, str (args), str(kwargs))

    else:
        cmd_str = command


    print "profile: %s" % cmd_str

    info = {'cmd' : cmd_str}


    # start stress, get it spinning for one min to et a confirmed load
    # measurement, then run our own load, then kill stress.
    if  _LOAD > 0 :
        rsu.logger.info ("creating system load %s" % _LOAD)
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        os.popen ('stress --cpu %s &' % _LOAD)
        time.sleep (60)

    time_1 = rsu.timestamp()
    load_1 = float(os.popen (_LOAD_CMD).read())

    start = rsu.timestamp()

    os.environ['_RADICAL_SYNAPSE_PROFILED'] = 'TRUE'

    # run the profiled function/command in a separate process
    if callable (command):

        proc = mp.Process (target = command,
                           args   = args,
                           kwargs = kwargs)
        proc.start ()

    else:

        proc = sp.Popen (command.split(),
                        stdout = sp.PIPE,
                        stderr = sp.STDOUT)

    watchers = list()
    watchers.append (rsw.WatcherCPU (proc.pid))
    watchers.append (rsw.WatcherIO  (proc.pid))
    watchers.append (rsw.WatcherMem (proc.pid))
    watchers.append (rsw.WatcherSys (proc.pid))

    if callable (command):

        proc.join()
        out = ""
        ret = None

    else:
        out = proc.communicate()[0]
        ret = proc.returncode

    stop = rsu.timestamp()

    info['time'] = dict()
    info['time']['start'] = rsu.time_zero()
    info['time']['real']  = stop-start

    for watcher in reversed(watchers) :
        watcher.stop ()
        watcher.join ()
        ru.dict_merge (info, watcher.get_data())

    # allow watchers to finalize some stuff, now having data from other watchers
    # available
    for watcher in reversed(watchers) :
        watcher.finalize(info)

    time_2 = rsu.timestamp()
    load_2 = float(os.popen (_LOAD_CMD).read())
    info['cpu']['load'] = max(load_1, load_2)
    rsu.logger.info ("system load %s: %s" % (_LOAD, info['cpu']['load']))
   
    if  _LOAD > 0 :
        rsu.logger.info ("stopping system load")
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        rsu.logger.info ("stopped  system load")

    if '_RADICAL_SYNAPSE_EMULATED' in os.environ:
        rsu.store_profile (info, emulated=True)
    else:
        rsu.store_profile (info, emulated=False)

    return info, ret, out


_CPU = 0
_MEM = 1
_STO = 2

# ------------------------------------------------------------------------------
#
def _emulator (samples) :

    atoms = dict()

    # create atoms for all sample types
    atoms[_CPU] = rsa.Compute ()
    atoms[_MEM] = rsa.Memory  ()
    atoms[_STO] = rsa.Storage ()

 #  app_n = rsa.Network ()

    # the atoms below are executed concurrently (in their own threads)
    app_c.run (info={'n'   : cpu_ops})   # consume  n CPU Ooperations
    app_m.run (info={'n'   : mem_size})  # allocate n Byte memory
    app_s.run (info={'n'   : io_write,   # write    n Byte to disk
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
   
    print "-------------------------------"

    info_c = app_c.stop ()
    info_m = app_m.stop ()
    info_s = app_s.stop ()
 #  info_n = app_n.stop ()

  # time_c = float(info_c['timer'])
  # time_m = float(info_m['timer'])
  # time_s = float(info_s['timer'])
 ## time_n = float(info_n['timer'])

  # host   = os.getenv ('HOST', os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ())
  # output = '%-10s %10s ------- %7.2f %7.2f %7.2f %5d %5d %5d %5d' % \
  #         (host, "", time_c, time_m, time_s,
  #          0, cpu_flops, mem_size, io_write)

  # print output
  # f.write ("%s\n" % output)



# ------------------------------------------------------------------------------
#
def emulate (command) :

    # FIXME: average vals over all retrieved profiles
    profs = rsu.get_profiles (command)
    prof  = profs[0]['profile']

    pprint.pprint (prof)

    # get time series to emulate (all types of operations are mixed)
    samples  = list()
    samples += [[_CPU, x[0], [x[1].get('ops',        0),
                              x[1].get('efficiency', 0)]] for x in prof['cpu']['sequence']]
    samples += [[_MEM, x[0], [x[1].get('size',       0)]] for x in prof['mem']['sequence']]
    samples += [[_STO, x[0], [x[1].get('read',       0), 
                              x[1].get('write',      0)]] for x in prof['i_o']['sequence']]

    # sort samples by time
    samples = sorted (samples, key=lambda x: x[1])

    pprint.pprint (samples)
    sys.exit()

    # let the profiler know that we run an emulation, so that the profile is not
    # stored as 'application run'.
    os.environ['_RADICAL_SYNAPSE_EMULATED'] = 'TRUE'

    new_info, ret, _ = profile (_emulator, samples)

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

