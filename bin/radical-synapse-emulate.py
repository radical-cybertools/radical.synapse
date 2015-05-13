#!/usr/bin/env python

import sys
import pprint
import radical.synapse

# FIXME: support tags as flags

if len(sys.argv) < 2 :
    print "\n\n\tusage: %s <command> ...\n\n" % sys.argv[0]
    sys.exit (0)

info, ret, out = radical.synapse.emulate (' '.join (sys.argv[1:]))

pprint.pprint (info)
print out

sys.exit (ret)

