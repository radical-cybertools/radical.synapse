

import os
import time

import synapse.atoms as sa


with open('%s/synapses.log' % os.environ['HOME'], 'a') as f :

    host  = os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ()
    stamp = time.ctime()
    start = time.time()

    # create containers for different system workload types
    sac = sa.Compute ()
    sam = sa.Memory  ()
    sas = sa.Storage ()
  # san = sa.Network ()
    
    # the atoms below are executed concurrently (in their own threads)
    sac.run (info={'n' : 10000}) # consume  10 GFlop CPY Cycles
    sam.run (info={'n' : 1000})  # allocate  1 GByte memory
    sas.run (info={'n' : 2000,   # write     2 GByte to disk
                   'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})
    
  # san.run (info={'type'   : 'server', # communicate a 1 MByte message
  #                'mode'   : 'read',
  #                'port'   : 10000,
  #                'n'      : 100})
  # time.sleep (1)
  # san.run (info={'type'   : 'client',
  #                'mode'   : 'write',
  #                'host'   : 'localhost',
  #                'port'   : 10000,
  #                'n'      : 100})
    
    # wait 'til all atoms are done
    times = {}
    times['c'] = sac.wait ()
    times['m'] = sam.wait ()
    times['s'] = sas.wait ()
  # times['n'] = san.wait ()
    
    # burn some more cyles, for the fun of it
    sac.run (info={'n' : 1}) # consume  1 GFlop CPY Cycles
    
    f.write ('%5s : %-10s : %4.2f : %s\n' % (os.getpid(), host, time.time() - start, times))

