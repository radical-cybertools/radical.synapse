
import synapse.atoms as sa
import time

# create containers for different system workload types
sac = sa.Compute ()
sam = sa.Memory  ()
sas = sa.Storage ()
san = sa.Network ()

# the atoms below are executed concurrently (in their own threads)
sac.run (info={'n' : 1000}) # consume  1 GFlop CPY Cycles
sam.run (info={'n' : 1000}) # allocate 1 GByte memory
sas.run (info={'n' : 1000,  # write    1 GByte to disk
               'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})

san.run (info={'type'   : 'server', # communicate a 1 GByte message
               'mode'   : 'read',
               'port'   : 10000,
               'n'      : 1000})
time.sleep (1)
san.run (info={'type'   : 'client',
               'mode'   : 'write',
               'host'   : 'localhost',
               'port'   : 10000,
               'n'      : 1000})

# wait 'til all atoms are done
sac.wait ()
sam.wait ()
sas.wait ()
san.wait ()

# burn some more cyles, for the fun of it
sac.run (info={'n' : 1000}) # consume  1 GFlop CPY Cycles

