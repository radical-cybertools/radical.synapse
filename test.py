
import synapse.atoms as sa

sac = sa.Compute ()
sam = sa.Memory  ()
sas = sa.Storage ()
san = sa.Network ()

sac.run (info={'n' : 100})
sam.run (info={'n' : 100})
sas.run (info={'n' : 100, 'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})
san.run (info={'type'   : 'server',
               'mode'   : 'read',
               'port'   : 10000,
               'n'      : 1})
san.run (info={'type'   : 'client',
               'mode'   : 'write',
               'host'   : 'localhost',
               'port'   : 10000,
               'n'      : 1})

sac.wait ()
sam.wait ()
sas.wait ()
san.wait ()

