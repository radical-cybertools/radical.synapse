#!/usr/bin/env python


import os
import sys
import time
import pprint
import radical.utils as ru

import radical.synapse       as rs
import radical.synapse.atoms as rsa

# import pudb 
# pudb.set_interrupt_handler ()

iters = 10
host  = os.getenv ('HOST', os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ())

# ------------------------------------------------------------------------------
#
def synaptic (load_compute, load_memory, load_input, load_output) :

    start = time.time()

    # create containers for different system workload types
    atoms = dict()
    atoms['c'] = rsa.Compute ()
    atoms['m'] = rsa.Memory  ()
    atoms['i'] = rsa.Storage ()
    atoms['o'] = rsa.Storage ()

    # the atoms below are executed concurrently (in their own threads)
    atoms['c'].run (info={'n'    : load_compute})
    atoms['m'].run (info={'n'    : load_memory})
    atoms['i'].run (info={'size' : load_input,
                          'mode' : 'r',
                          'tgt'  : '/tmp/src'})
    atoms['o'].run (info={'size' : load_output,
                          'mode' : 'w'})

    # wait for all atom threads to be done
    info_c = atoms['c'].wait ()
    info_m = atoms['m'].wait ()
    info_i = atoms['i'].wait ()
    info_o = atoms['o'].wait ()

    for info in [info_c, info_m, info_i, info_o] :
        for line in info['out'] :
            l = ru.ReString (line)
            if  l // '^(ru.\S+)\s+:\s+(\S+)$' :
                info[l.get()[0]] = l.get()[1]

    print("------------------------------")
    pprint.pprint (info_i)
    print("------------------------------")
    pprint.pprint (info_o)
    print("------------------------------")



# ------------------------------------------------------------------------------
#
#
cfg_list = list ()

if  not len(sys.argv) > 1 :
    print("\n\tusage: %s [-c n] [-m n] [-i n] [-o n] \n\n" % sys.argv[0])
    sys.exit (-1)

load_compute = 0
load_memory  = 0
load_input   = 0
load_output  = 0

for i in range(len(sys.argv)) :

    if sys.argv[i] == '-c' : load_compute = int(sys.argv[i+1])
    if sys.argv[i] == '-m' : load_memory  = int(sys.argv[i+1])
    if sys.argv[i] == '-i' : load_input   = int(sys.argv[i+1])
    if sys.argv[i] == '-o' : load_output  = int(sys.argv[i+1])


synaptic (load_compute, load_memory, load_input, load_output)

print(load_compute)
print(load_memory)
print(load_input)
print(load_output)

  
