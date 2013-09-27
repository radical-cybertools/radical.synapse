
import synapse.atoms as sa

sac = sa.Compute ()
sam = sa.Memory  ()
sas = sa.Storage ()

sac.run (info={'n' : 1000})
sam.run (info={'n' : 1000})
sas.run (info={'n' : 1000, 'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})

sac.wait ()
sam.wait ()
sas.wait ()

