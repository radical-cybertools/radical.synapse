#!/usr/bin/env python


import os
import sys
import time
import numpy
import pprint        as pp
import radical.utils as ru

import radical.synapse       as rs
import radical.synapse.atoms as rsa

# import pudb 
# pudb.set_interrupt_handler ()

iters = 10
host  = os.getenv ('HOST', os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ())

# ------------------------------------------------------------------------------
#
def synaptic (load_compute, load_memory, load_storage) :

    start = time.time()

    # create containers for different system workload types
    atoms = dict()
    atoms['c'] = rsa.Compute ()
    atoms['m'] = rsa.Memory  ()
    atoms['s'] = rsa.Storage ()

    # the atoms below are executed concurrently (in their own threads)
    atoms['c'].run (info={'n'   : load_compute})
    atoms['m'].run (info={'n'   : load_memory})
    atoms['s'].run (info={'n'   : load_storage,
                          'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})

    # wait for all atom threads to be done
    info_c = atoms['c'].wait ()
    info_m = atoms['m'].wait ()
    info_s = atoms['s'].wait ()

    for info in [info_c, info_m, info_s] :
        for line in info['out'] :
            l = ru.ReString (line)
            if  l // '^(ru.\S+)\s+:\s+(\S+)$' :
                info[l.get()[0]] = l.get()[1]

    return {'c':info_c, 'm':info_m, 's':info_s}


# ------------------------------------------------------------------------------
#

def main (cfg_list) :

    n2h = rs.number_to_human

    for cfg in cfg_list :
        x       = int  (cfg[ 2])
        y       = int  (cfg[ 3])
        z       = int  (cfg[ 4])
        stress  = int  (cfg[ 5])
        compute = float(cfg[10])
        util    = float(cfg[11])
        eff     = float(cfg[12])
        load    = float(cfg[13])
        memory  = float(cfg[14])
        storage = float(cfg[15])

        iter_1_time = list()
        iter_1_cpu  = list()
        iter_1_mem  = list()
        iter_1_io   = list()
        iter_1_util = list()
        iter_1_eff  = list()
        iter_1_sys  = list()

        for iter in range (iters) :

            info_emu, ret, out = rs.profile (synaptic, compute, memory, storage)

            if not 'utilization' in info_emu['cpu'] : info_emu['cpu']['utilization' ] = 0
            if not 'efficiency'  in info_emu['cpu'] : info_emu['cpu']['efficiency'  ] = 0
            if not 'load'        in info_emu['cpu'] : info_emu['cpu']['load'        ] = 0
            if not 'ops'         in info_emu['cpu'] : info_emu['cpu']['ops'         ] = 0
            if not 'max'         in info_emu['mem'] : info_emu['mem']['max'         ] = 0
            if not 'write'       in info_emu['io']  : info_emu['io']['write'        ] = 0
        
            load_compute = int(float(info_emu['cpu']['ops' ]) / (1024*1024) / 8)
            load_memory  = int(float(info_emu['mem']['max' ]) / (1024*1024))
            load_storage = int(float(info_emu['io']['write']) / (1024*1024))
            
            load_compute = int(float(info_emu['cpu']['ops' ]) / (1024*1024) / 8)
            load_memory  = int(float(info_emu['mem']['max' ]) / (1024*1024))
            load_storage = int(float(info_emu['io']['write']) / (1024*1024))
            
            load_id  = 'EMU.%04d' % x
            output   = '%-10s %15s %5d %5d %5d %6d %8.2f --------- --------- --------- %9.2f %0.2f %0.2f %5.2f %9.2f %9.2f' % \
                       (host, load_id, x, y, z, stress,
                        float(info_emu['time']['real']), 
                        load_compute, 
                        info_emu['cpu']['utilization'], 
                        info_emu['cpu']['efficiency'], 
                        info_emu['sys']['load'],
                        load_memory, 
                        load_storage
                       )
            print output

            iter_1_time .append(float(info_emu['time']['real']))
            iter_1_cpu  .append(float(load_compute))
            iter_1_mem  .append(float(load_memory))
            iter_1_io   .append(float(load_storage))
            iter_1_util .append(float(info_emu['cpu']['utilization']))
            iter_1_eff  .append(float(info_emu['cpu']['efficiency']))
            iter_1_sys  .append(float(info_emu['sys']['load']))

        iter_1_mean_time = numpy.mean (numpy.array (iter_1_time))
        iter_1_mean_cpu  = numpy.mean (numpy.array (iter_1_cpu ))
        iter_1_mean_mem  = numpy.mean (numpy.array (iter_1_mem ))
        iter_1_mean_io   = numpy.mean (numpy.array (iter_1_io  ))
        iter_1_mean_util = numpy.mean (numpy.array (iter_1_util))
        iter_1_mean_eff  = numpy.mean (numpy.array (iter_1_eff ))
        iter_1_mean_sys  = numpy.mean (numpy.array (iter_1_sys ))
    
        iter_1_std_time  = numpy.std  (numpy.array (iter_1_time))
        iter_1_std_cpu   = numpy.std  (numpy.array (iter_1_cpu ))
        iter_1_std_mem   = numpy.std  (numpy.array (iter_1_mem ))
        iter_1_std_io    = numpy.std  (numpy.array (iter_1_io  ))
        iter_1_std_util  = numpy.std  (numpy.array (iter_1_util))
        iter_1_std_eff   = numpy.std  (numpy.array (iter_1_eff ))
        iter_1_std_sys   = numpy.std  (numpy.array (iter_1_sys ))
        
        load_id  = 'MEAN_EMU.%04d' % x
        mean     = '%-10s %15s %5d %5d %5d %5d %9.2f --------- --------- --------- %9.2f %.2f %.2f %5.2f %9.2f %9.2f' % \
                   (host, load_id, x, y, z, stress,
                    iter_1_mean_time, 
                    iter_1_mean_cpu,
                    iter_1_mean_util, 
                    iter_1_mean_eff, 
                    iter_1_mean_sys,
                    iter_1_mean_mem, 
                    iter_1_mean_io
                   )
        print mean  
    
        load_id  = 'STD_EMU.%04d' % x
        std      = '%-10s %15s %5d %5d %5d %5d %9.2f --------- --------- --------- %9.2f %.2f %.2f %5.2f %9.2f %9.2f' % \
                   (host, load_id, x, y, z, stress, 
                    iter_1_std_time, 
                    iter_1_std_cpu,
                    iter_1_std_util, 
                    iter_1_std_eff, 
                    iter_1_std_sys,
                    iter_1_std_mem, 
                    iter_1_std_io
                   )
        print std
    
        load_id  = 'STAT_EMU.%04d' % x
        stat     = '%-10s %15s %5d %5d %5d %5d %9.2f %9.2f --------- --------- --------- --------- --------- --------- %9.2f %9.2f %.2f %.2f %.2f %.2f %5.2f %5.2f %9.2f %9.2f %9.2f %9.2f' % \
                   (host, load_id, x, y, z, stress, 
                    iter_1_mean_time, 
                    iter_1_std_time, 
                    iter_1_mean_cpu,
                    iter_1_std_cpu,
                    iter_1_mean_util, 
                    iter_1_std_util, 
                    iter_1_mean_eff, 
                    iter_1_std_eff, 
                    iter_1_mean_sys,
                    iter_1_std_sys,
                    iter_1_mean_mem, 
                    iter_1_std_mem, 
                    iter_1_mean_io,
                    iter_1_std_io
                   )
        print stat  
    
# ------------------------------------------------------------------------------
#
#
cfg_list = list ()

if  not len(sys.argv) > 1 :
    print "\n\tusage: %s <cfg_file> \n\n" % sys.argv[0]
    sys.exit (-1)

with open (sys.argv[1]) as fin :
    lines = fin.readlines ()

for line in lines :
    line = line.replace ('\n', '')
    re = ru.ReString (line)
    if  re // r'(MEAN_PRO)' :
        print line
        cfg_list.append (line.split())

main (cfg_list)

  
