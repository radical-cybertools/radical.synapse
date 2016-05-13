
import os
import sys
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
LOAD = int (os.environ.get ('LOAD', '0'))

if 'darwin' not in sys.platform.lower():
  # LOAD_CMD    = "top -b -n1 | head -1  |       cut -f 4 -d :         | cut -f 1 -d ,"
    LOAD_CMD    = "top -b -n1 | head -n1 | rev | cut -f 3 -d \  | rev  | sed -e 's/,//'"
else:
    LOAD_CMD    = "top -l 1 | head -n 3 | tail -n 1 | cut -f 3 -d ' ' | cut -f 1 -d ','"



# ------------------------------------------------------------------------------
#
def execute (command, *args, **kwargs) :

    if callable (command):
        cmd_str = "%s %s %s" % (command.__name__, str (args), str(kwargs))

    else:
        cmd_str = command


    print "execute: %s" % cmd_str

    info = {'cmd' : cmd_str}


    # start stress, get it spinning for one min to get a confirmed load
    # measurement, then run our own load, then kill stress.
    if  LOAD > 0 :
        rsu.logger.info ("creating system load %s" % LOAD)
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        os.popen ('stress --cpu %s &' % LOAD)
        time.sleep (60)

    load_1 = float(os.popen (LOAD_CMD).read())
    start  = rsu.timestamp()

    os.environ['_RADICAL_SYNAPSE_PROFILED'] = 'TRUE'

    # run the function/command in a separate process
    if callable (command):

        proc = mp.Process (target = command,
                           args   = args,
                           kwargs = kwargs)
        proc.start ()

    else:

        proc = sp.Popen (command.split(),
                        stdout = sp.PIPE,
                        stderr = sp.STDOUT)

    if callable (command):

        proc.join()
        out = ""
        ret = None

    else:
        out = proc.communicate()[0]
        ret = proc.returncode

    stop   = rsu.timestamp()
    load_2 = float(os.popen (LOAD_CMD).read())

    info['time'] = dict()
    info['time']['start'] = rsu.time_zero()
    info['time']['real']  = stop-start

    info['cpu']  = dict()
    info['cpu']['load']   = max(load_1, load_2)
   
    if  LOAD > 0 :
        rsu.logger.info ("stopping system load")
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        rsu.logger.info ("stopped  system load")

    return info, ret, out


# ------------------------------------------------------------------------------
#
def profile (command, *args, **kwargs) :

    if callable (command):
        cmd_str = "%s %s %s" % (command.__name__, str (args), str(kwargs))

    else:
        cmd_str = command


    print "profile: %s" % cmd_str

    if '_RADICAL_SYNAPSE_EMULATED' in os.environ:
        cmd_str = os.environ.get ('_RADICAL_SYNAPSE_EMULATEE', cmd_str)
        print 'using emulated command name: %s' % cmd_str

    info = {'cmd' : cmd_str}

    # start stress, get it spinning for one min to get a confirmed load
    # measurement, then run our own load, then kill stress.
    if  LOAD > 0 :
        rsu.logger.info ("creating system load %s" % LOAD)
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        os.popen ('stress --cpu %s &' % LOAD)
        time.sleep (60)

    load_1 = float(os.popen (LOAD_CMD).read())
    start  = rsu.timestamp()

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

    watch_mode = os.environ.get('RADICAL_SYNAPSE_WATCHMODE', 'full').lower()
    watchers   = list()

    if watch_mode == 'full':
        watchers.append (rsw.WatcherCPU (proc.pid))
        watchers.append (rsw.WatcherSto (proc.pid))
        watchers.append (rsw.WatcherMem (proc.pid))

    # watchmode 'basic'
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
    load_2 = float(os.popen (LOAD_CMD).read())
    info['cpu']['load'] = max(load_1, load_2)
    rsu.logger.info ("system load %s: %s" % (LOAD, info['cpu']['load']))
   
    if  LOAD > 0 :
        rsu.logger.info ("stopping system load")
        os.popen ("killall -9 stress 2>&1 > /dev/null")
        rsu.logger.info ("stopped  system load")

    return info, ret, out


_CPU = 'cpu'
_MEM = 'mem'
_STO = 'sto'
_TIM = 'time'

_TYPE = 0
_TIME = 1
_VALS = 2

# ------------------------------------------------------------------------------
#
def _emulator (samples) :

    atoms = dict()  # one atom of eeach type
    state = dict()  # there is at most one atom for each type in 'state'

    # create atoms for all sample types
    atoms[_TIM] = rsa.Time    ()
    atoms[_CPU] = rsa.Compute ()
    atoms[_MEM] = rsa.Memory  ()
    atoms[_STO] = rsa.Storage ()

    # FIXME: make sure threads and queues are up
    time.sleep (0.1)

    print "\n-------------------------\n\n"
    print "emulating %d samples" % len(samples)

    # run the first set of samples until we meet a sample type which is already
    # started.  At that point, start to wait before submission.  If all samples
    # have been run, wait for all atoms to complete, and voila
    for pre in range(len(samples)):

        t = samples[pre][_TYPE]
        v = samples[pre][_VALS]

        if not t in state:
            # no such atom running - start one
            atoms[t].emulate (v)
            state[t] = atoms[t]

            print 'pre %d : %s' % (pre, t)

        else:
            # such an atom is running -- go into steady state to wait for # it
            print 'brk %d : %s' % (pre, t)
            break


    # we need to wait first before running the next sample of any type
    for idx in range(pre,len(samples)):

        t = samples[idx][_TYPE]
        v = samples[idx][_VALS]

        if t in state:
            print 'wai %d : %s' % (idx, t)
            state[t].wait()
        else:
            print 'cre %d : %s' % (idx, t)
            state[t] = atoms[t]

        print 'idx %d : %s' % (idx, t)
        state[t].emulate(v)


    # all samples are running now (or have been running), now wait for all
    # active ones
    for t in state:
        print 'wai   : %s' % t
        state[t].wait()


    # we are done and can shut the atoms down
    for t in atoms:
        atoms[t].stop()

    print "\n-------------------------\n\n"


# ------------------------------------------------------------------------------
#
def emulate(command=None, samples=None, src=None):

    if (command and samples) or \
       (command and src    ) or \
       (samples and src    )    :
        raise ValueError ("emulate needs *either* command, sample *or* src")

    if not command and not samples and not src:
        raise ValueError ("emulate needs either command, sample or src")

    if command or src:

        if command:
            # FIXME: average vals over all retrieved profiles
            profs = rsu.get_profiles (command, mode='pro')
            prof  = profs[0]['profile']

        else:
            prof = ru.read_json(src)

        pprint.pprint (prof)

        # get time series to emulate (all types of operations are mixed)
        # FIXME: we should also sample walltime for _TIM.  As it is, mixing
        #        time and other samples will yield incorrect results due to
        #        mismatch in granularity.
        samples  = list()
      # samples += [[_TIM, x[0], [x[1].get('real',       0.0)]] for x in prof['time']]
        samples += [[_CPU, x[0], [x[1].get('ops',        0)  ,
                                  x[1].get('efficiency', 0)  ]] for x in prof['cpu']['sequence']]
        samples += [[_MEM, x[0], [x[1].get('size',       0)  ]] for x in prof['mem']['sequence']]
        samples += [[_STO, x[0], [x[1].get('read',       0)  , 
                                  x[1].get('write',      0)  ]] for x in prof['sto']['sequence']]

    # sort samples by time
    samples = sorted (samples, key=lambda x: x[1])

    print "samples:\n---"
    pprint.pprint (samples)
    print "---"

    watchmode = os.environ.get ('RADICAL_SYNAPSE_WATCHMODE')
    if not watchmode or watchmode.lower in ['none', 'noop']:
        start = time.time()
        _emulator (samples)
        stop  = time.time()

        ret   = None
        info  = dict()
        info['cmd']  = command
        info['time'] = dict()
        info['time']['start'] = start
        info['time']['real']  = stop-start

    else:
        # let the profiler know that we run an emulation, so that the profile is not
        # stored as 'application run'.
        os.environ['_RADICAL_SYNAPSE_EMULATED'] = 'TRUE'
        os.environ['_RADICAL_SYNAPSE_EMULATEE'] = command

        info, ret, _ = profile (_emulator, samples)

        if 'ops' in info['cpu']:
            info['cpu']['efficiency'] = info['cpu']['ops']                       \
                                        / ( info['cpu']['ops']                   \
                                          + info['cpu']['cycles_stalled_front']  \
                                          + info['cpu']['cycles_stalled_back']   \
                                          )

       #print 'efficiency = %s / (%s + %s + %s) = %s' % (
       #          info['cpu']['ops'],
       #          info['cpu']['ops'],
       #          info['cpu']['cycles_stalled_front'],
       #          info['cpu']['cycles_stalled_back'],
       #          info['cpu']['efficiency'])


    return (info, ret, None)




# ------------------------------------------------------------------------------

