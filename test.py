
import synapse.atoms as sa

sac = sa.Compute ()
sam = sa.Memory  ()
sas = sa.Storage ()

sac.run (info={'n_compute' : 1000})
sam.run (info={'n_memory'  : 1000})
sas.run (info={'n_storage' : 1000})

sac.wait ()
sam.wait ()
sas.wait ()

