

import os
import sys
import time
import pprint
import threading

import radical.synapse       as rs
import radical.synapse.atoms as rsa

os.environ['RADICAL_SYNAPSE_DBURL'] = "file://%s" % os.getcwd ()
print os.environ['RADICAL_SYNAPSE_DBURL']


print "------------------------------------------------------------------------"
os.environ['RADICAL_SYNAPSE_TAGS']  = "cpu"
info, _, _ = rs.emulate ('test cpu')
pprint.pprint (info)

print "------------------------------------------------------------------------"
os.environ['RADICAL_SYNAPSE_TAGS']  = "mem"
info, _, _ = rs.emulate ('test mem')
pprint.pprint (info)

print "------------------------------------------------------------------------"
os.environ['RADICAL_SYNAPSE_TAGS']  = "sto"
info, _, _ = rs.emulate ('test sto')
pprint.pprint (info)

print "------------------------------------------------------------------------"
os.environ['RADICAL_SYNAPSE_TAGS']  = ""
info, _, _ = rs.emulate ('test')
pprint.pprint (info)


print "------------------------------------------------------------------------"
info, _, _ = rs.execute ('sleep 3')
pprint.pprint (info)

print "------------------------------------------------------------------------"
info, _, _ = rs.profile ('sleep 3')
pprint.pprint (info)

print "------------------------------------------------------------------------"
info, _, _ = rs.emulate ('sleep 3')
pprint.pprint (info)

print "------------------------------------------------------------------------"

