

import os
import sys
import time
import pprint
import threading

import radical.synapse       as rs
import radical.synapse.atoms as rsa

os.environ['RADICAL_SYNAPSE_DBURL'] = "file://%s" % os.getcwd ()
os.environ['RADICAL_SYNAPSE_TAGS']  = "sto:sto"
print os.environ['RADICAL_SYNAPSE_DBURL']

info, _, _ = rs.emulate ('test sto')

pprint.pprint (info)

