#!/usr/bin/env python

import sys
import time
import pprint
import radical.synapse

# FIXME: support tags as flags

if len(sys.argv) < 2 :
    print "\n\n\tusage: %s <command> ...\n\n" % sys.argv[0]
    sys.exit (0)

info, ret, out = radical.synapse.profile (' '.join (sys.argv[1:]))
# info, ret, out = radical.synapse.profile (time.sleep, 10)

print out
pprint.pprint (info)

sys.exit (ret)

