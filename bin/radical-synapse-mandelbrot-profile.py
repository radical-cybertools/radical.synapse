#!/usr/bin/env python


import os
import sys
import time
import numpy
import pprint        as pp
import radical.utils as ru

import synapse as rs

# import pudb 
# pudb.set_interrupt_handler ()

iters = 10
host  = os.getenv ('HOST', os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ())

# ------------------------------------------------------------------------------
#
def mandel (x, y, z) :

  # print 'mandel: %s %s %s' % (x, y, z)

    start = time.time ()

    x_pixels  = x
    y_pixels  = y
    iter_max  = z
    x_min     = -2.0
    x_max     = +1.0
    y_min     = -1.5
    y_max     = +1.5
    threshold = 1
    rgb_image = []

    for x in range (x_pixels) :

      # print x

        cx = x * (x_max - x_min) / x_pixels + x_min

        rgb_row = []

        for y in range (y_pixels):

            cy = y * (y_max - y_min) / (y_pixels - 1) + x_min

            c = complex (cx, cy)
            z = 0

            for i in range (iter_max) :
                
                if abs (z) > threshold: 
                    break 

                z = z * z + c 

            rgb_row.append (["%3d" % i, "%3d" % i, "%3d" % i])

        rgb_image.append (rgb_row)

    with open ("/tmp/mb.dat", "w") as f :
        f.write (str(rgb_image))

    stop = time.time ()

    return stop - start


# ------------------------------------------------------------------------------
#

def main (cfg_list) :

    n2h = rs.number_to_human

    for cfg in cfg_list :
        x       = int  (cfg[ 2])
        y       = int  (cfg[ 3])
        z       = int  (cfg[ 4])
        stress  = 0
        compute = 0
        util    = 0
        eff     = 0
        load    = 0
        memory  = 0
        storage = 0

        iter_1_time = list()
        iter_1_cpu  = list()
        iter_1_mem  = list()
        iter_1_io   = list()
        iter_1_util = list()
        iter_1_eff  = list()
        iter_1_sys  = list()

        for iter in range (iters) :

            info_run, ret, out = rs.profile (mandel, x, y, z)

            if not 'utilization' in info_run['cpu'] : info_run['cpu']['utilization' ] = 0
            if not 'efficiency'  in info_run['cpu'] : info_run['cpu']['efficiency'  ] = 0
            if not 'load'        in info_run['cpu'] : info_run['cpu']['load'        ] = 0
            if not 'ops'         in info_run['cpu'] : info_run['cpu']['ops'         ] = 0
            if not 'max'         in info_run['mem'] : info_run['mem']['max'         ] = 0
            if not 'write'       in info_run['io']  : info_run['io']['write'        ] = 0
        
            load_compute = int(float(info_run['cpu']['ops' ]) / (1024*1024) / 8)
            load_memory  = int(float(info_run['mem']['max' ]) / (1024*1024))
            load_storage = int(float(info_run['io']['write']) / (1024*1024))
            
            load_compute = int(float(info_run['cpu']['ops' ]) / (1024*1024) / 8)
            load_memory  = int(float(info_run['mem']['max' ]) / (1024*1024))
            load_storage = int(float(info_run['io']['write']) / (1024*1024))
            
            load_id  = 'RUN.%04d' % x
            output   = '%-10s %15s %5d %5d %5d %6d %8.2f --------- --------- --------- %9.2f %0.2f %0.2f %5.2f %9.2f %9.2f' % \
                       (host, load_id, x, y, z, stress,
                        ret, 
                        load_compute, 
                        info_run['cpu']['utilization'], 
                        info_run['cpu']['efficiency'], 
                        info_run['sys']['load'],
                        load_memory, 
                        load_storage
                       )
            print output

            iter_1_time .append(float(ret))
            iter_1_cpu  .append(float(load_compute))
            iter_1_mem  .append(float(load_memory))
            iter_1_io   .append(float(load_storage))
            iter_1_util .append(float(info_run['cpu']['utilization']))
            iter_1_eff  .append(float(info_run['cpu']['efficiency']))
            iter_1_sys  .append(float(info_run['sys']['load']))

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
        
        load_id  = 'MEAN_RUN.%04d' % x
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
    
        load_id  = 'STD_RUN.%04d' % x
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
    
        load_id  = 'STAT_RUN.%04d' % x
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

  
