#!/usr/bin/env python

import sys
import pprint
import radical.synapse

if len(sys.argv) != 2 :
    print "\n\n\tusage: %s <command>\n\n" % sys.argv[0]
    sys.exit (0)

info, ret, out = radical.synapse.emulate_command (sys.argv[1])

pprint.pprint (info)
print out

sys.exit (ret)

