

import os
import time

import synapse.atoms as sa


with open ('./test.dat', 'a') as f :

    sync  = os.popen ('rm -rf /tmp/synapse/')
    sync  = os.popen ('sync')
    host  = os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ()
    stamp = time.ctime()
    start = time.time()

    load_id        = str(os.environ['SYNAPSE_ID'])
    load_instances = int(os.environ['SYNAPSE_INSTANCES'])
    load_compute   = int(os.environ['SYNAPSE_COMPUTE_GFLOPS'])
    load_memory    = int(os.environ['SYNAPSE_MEMORY_GBYTES' ])
    load_storage   = int(os.environ['SYNAPSE_STORAGE_GBYTES'])

    apps = list()

    # create containers for different system workload types
    for i in range (0, load_instances) :

        app = dict()
        app['c'] = sa.Compute ()
        app['m'] = sa.Memory  ()
        app['s'] = sa.Storage ()
      # app['n'] = sa.Network ()

        apps.append (app)


    # run load (this spawns threads as quickly as possible)
    for app in apps :

        # the atoms below are executed concurrently (in their own threads)
        app['c'].run (info={'n'   : load_compute})  # consume  10 GFlop CPY Cycles
        app['m'].run (info={'n'   : load_memory})   # allocate  5 GByte memory
        app['s'].run (info={'n'   : load_storage,   # write     2 GByte to disk
                            'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})

      # app['n'].run (info={'type'   : 'server', # communicate a 1 MByte message
      #                     'mode'   : 'read',
      #                     'port'   : 10000,
      #                     'n'      : 100})
      # time.sleep (1)
      # app['n'].run (info={'type'   : 'client',
      #                     'mode'   : 'write',
      #                     'host'   : 'localhost',
      #                     'port'   : 10000,
      #                     'n'      : 100})


    # all are started -- now wait for completion and collect times
    times = {}
    times['c'] = 0.0
    times['m'] = 0.0
    times['s'] = 0.0
  # times['n'] = 0.0

    cid = 0
    for app in apps :
        cid += 1

        t_c = float (app['c'].wait ())
        t_m = float (app['m'].wait ())
        t_s = float (app['s'].wait ())
      # t_n = float (app['n'].wait ())

        times['c'] += t_c
        times['m'] += t_m
        times['s'] += t_s
      # times['n'] += t_n

        output = '%-10s %10s ------- %7.2f %7.2f %7.2f %5d %5d %5d %5d' % \
                (host, "%s.%002d" % (load_id, cid), t_c, t_m, t_s,
                 load_instances, load_compute, load_memory, load_storage)

        print output
        f.write ("%s\n" % output)


    # also print summary
    output = '%-10s %7s    %7.2f ------- ------- ------- %5d %5d %5d %5d' % \
             (host, load_id, time.time() - start, 
             load_instances, load_compute, load_memory, load_storage)

    print output
    f.write ("%s\n" % output)

