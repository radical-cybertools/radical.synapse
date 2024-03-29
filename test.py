#!/usr/bin/env python3

import os
import sys
import time
import threading

from   pprint import pprint

import radical.synapse       as rs
import radical.synapse.atoms as rsa

os.environ['RADICAL_SYNAPSE_DBURL'] = "file://%s" % os.getcwd()
os.environ['RADICAL_SYNAPSE_TAGS']  = "cpu:cpu"
print(os.environ['RADICAL_SYNAPSE_DBURL'])
info, _, _ = rs.emulate('test cpu')

sys.exit

# ------------------------------------------------------------------------------
#
# info, ret, out = rs.profile('md5sum /tmp/l')
info, _, _ = rs.emulate('md5sum /tmp/l')
pprint(info)

sys.exit()


# ------------------------------------------------------------------------------
#
def testme(delay) :

    def _testme(d):

        f = open("/tmp/l")
        for i in range(1000000):
            data = f.read(20)
        f.close()

    time.sleep(0.1)
    t = threading.Thread(target=_testme, args=(delay,))
    t.start()
    t.join()
    time.sleep(0.1)

info, ret, out = rs.profile(testme, 10)
pprint(info)

sys.exit()


# ------------------------------------------------------------------------------
#
def func():
    c = rsa.Storage()
    m = rsa.Memory()
    s = rsa.Storage()

    for i in range(3):
        c.run({'n' : 1000})
        m.run({'n' : 1000})
        s.run({'n' : 1000})
        i = c.wait()
        i = m.wait()
        i = s.wait()

    c.stop()
    m.stop()
    s.stop()

rs.emulate('sleep 10')


command = rs.synapsify('sleep 10', rs.NOTHING)
command = rs.synapsify('sleep 10', rs.PROFILE)
command = rs.synapsify('sleep 10', rs.EMULATE)

info, ret, out = rs.emulate('sleep 10');
pprint(info)

sys.exit(0)

host  = os.getenv('HOST', os.popen('hostname | cut -f 1 -d . | xargs echo -n').read())
home  = os.getenv('HOME')

with open('%s/synapse/experiments/%s.dat' % (home, host), 'a') as f :

    _     = os.popen('sync')
#   _     = os.popen('rm -rf /tmp/synapse_*')
#   _     = os.popen('sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"')

    start = time.time()


    load_id        = str(os.environ.get('SYNAPSE_ID',           'X'))
    load_instances = int(os.environ.get('SYNAPSE_INSTANCES',      1))
    load_compute   = int(os.environ.get('SYNAPSE_COMPUTE_GFLOPS', 0))
    load_memory    = int(os.environ.get('SYNAPSE_MEMORY_GBYTES' , 0))
    load_storage   = int(os.environ.get('SYNAPSE_STORAGE_GBYTES', 0))

    apps = list()

    # create containers for different system workload types
    for i in range(0, load_instances) :

        app = dict()
        app['c'] = rsa.Compute()
        app['m'] = rsa.Memory ()
        app['s'] = rsa.Storage()
      # app['n'] = rsa.Network()

        apps.append(app)


    # run load (this spawns threads as quickly as possible)
    for app in apps :

        # the atoms below are executed concurrently (in their own threads)
        app['c'].run(info={'n'   : load_compute})  # consume  10 GFlop CPY Cycles
        app['m'].run(info={'n'   : load_memory})   # allocate  5 GByte memory
        app['s'].run(info={'n'   : load_storage,   # write     2 GByte to disk
                           'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})

      # app['n'].run(info={'type'   : 'server', # communicate a 1 MByte message
      #                    'mode'   : 'read',
      #                    'port'   : 10000,
      #                    'n'      : 100})
      # time.sleep(1)
      # app['n'].run(info={'type'   : 'client',
      #                    'mode'   : 'write',
      #                    'host'   : 'localhost',
      #                    'port'   : 10000,
      #                    'n'      : 100})


    # all are started -- now wait for completion and collect times
    times = {}
    times['c'] = 0.0
    times['m'] = 0.0
    times['s'] = 0.0
  # times['n'] = 0.0

    cid = 0
    for app in apps :
        cid += 1

        info_c = app['c'].wait()
        info_m = app['m'].wait()
        info_s = app['s'].wait()
      # info_n = app['n'].wait()

        t_c    = float(info_c['timer'])
        t_m    = float(info_m['timer'])
        t_s    = float(info_s['timer'])
      # t_n    = float(info_n['timer'])

      # import pprint
      # pprint.pprint(info_c)

        times['c'] += t_c
        times['m'] += t_m
        times['s'] += t_s
      # times['n'] += t_n

        output = '%-10s %10s ------- %7.2f %7.2f %7.2f %5d %5d %5d %5d' % \
                (host, "%s.%002d" % (load_id, cid), t_c, t_m, t_s,
                 load_instances, load_compute, load_memory, load_storage)

      # print output
        f.write("%s\n" % output)


    # also print summary
    output = '%-10s %7s    %7.2f ------- ------- ------- %5d %5d %5d %5d' % \
             (host, load_id, time.time() - start,
             load_instances, load_compute, load_memory, load_storage)

    print(output)
    f.write("%s\n" % output)

#   time.sleep(10)
    _ = os.popen('ps -ef | grep -i "/tmp/synapse_" | grep -v grep | cut -c 8-15 | xargs -r kill -9')

    print(rs.get_mem_usage())
    print(rs.get_io_usage())

