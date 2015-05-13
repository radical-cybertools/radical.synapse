#!/usr/bin/env python


import os
import sys
import time
import numpy
import pprint        as pp
import radical.utils as ru
import subprocess    as sp

import radical.synapse       as rs
import radical.synapse.atoms as rsa

# import pudb 
# pudb.set_interrupt_handler ()


host     = os.getenv ('HOST', os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ())
iters    = 10
mult_mem = 1
mult_io  = 10

# ------------------------------------------------------------------------------
#
def mandel (x=1024, y=1024, z=100) :

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
    images    = list()

    for l in range (mult_mem) :
        images.append (list())

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

        for l in range (mult_mem) :
            images[l].append (rgb_row)

    with open ("/tmp/mb.dat", "w") as f :
        for s in range (mult_io) :
            f.write (str(images[0]))


# ------------------------------------------------------------------------------
#
def synaptic (x, y, z, load_compute, load_memory, load_storage) :

    load_instances = 1

  # load_id = 'EMU.%04d' % x
  # print 'synaptic: %s %s %s' % (x, y, z)
  # print      '%8s: %s %s %s' % (load_id, load_compute, load_memory, load_storage)

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

n2h = rs.number_to_human

# host        load_id     t_real --------- --------- ---------     ?      load util  eff    load load_memory load_storage     x     y     z
header   = '%-10s %15s %5s %5s %5s stress   t_real     t_cpu     t_mem      t_io %9s %4s %4s %5s %9s %9s' % \
           ('# host', 'id', 'x', 'y', 'z', 'cpu', 'util', 'eff', 'load', 'mem', 'io')
print header

for stress in range(12,13) :
  # repeat first experiment, for warmup
  # for x in [10, 10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240] :
    for x in [2560] :
        for z in [250] : 

            y = x

            if  stress :
                s = str (stress)
                stresser = sp.Popen (["stress", "-q", "-c", s],
                                     stdout=None, stderr=None)

                time.sleep (5) # warmup time
    
    
            # --------------------------------------------------------------------------------------------
    
            iter_0_time = list()
    
            for iter in range (iters) :
    
                start = time.time ()
                mandel (x, y, z)
                stop  = time.time ()
    
                iter_0_time.append (stop - start)

                load_id  = 'EXE.%04d' % x
                stat_exe   = '%-10s %15s %5s %5s %5s %5d %9.2f' % \
                               (host, load_id, x, y, z, stress, stop-start)
                print stat_exe
    
            iter_0_mean_time = numpy.mean (numpy.array (iter_0_time))
            iter_0_std_time  = numpy.std  (numpy.array (iter_0_time))
    
            load_id  = 'STAT_EXE.%04d' % x
            stat_0   = '%-10s %15s %5s %5s %5s %5d %9.2f %9.2f' % \
                           (host, load_id, x, y, z, stress, 
                            iter_0_mean_time, iter_0_std_time)
            print stat_0

          # sp.call ("killall    stress", shell=True)
          # sp.call ("killall -9 stress", shell=True)
          #
          # continue
    
    
            # --------------------------------------------------------------------------------------------
            iter_1_time = list()
            iter_1_cpu  = list()
            iter_1_mem  = list()
            iter_1_io   = list()
            iter_1_util = list()
            iter_1_eff  = list()
            iter_1_sys  = list()
    
            for iter in range (iters) :
    
                info_pro, ret, out = rs.profile (mandel, x, y, z)
    
                load_compute = float(info_pro['cpu']['ops' ]) / (1024*1024) / 8
                load_memory  = float(info_pro['mem']['peak']) / (1024*1024)
                load_storage = float(info_pro['io']['write']) / (1024*1024)
    
                load_id  = 'PRO.%04d' % x
                output   = '%-10s %15s %5d %5d %5d %5d %9.2f --------- --------- --------- %9.2f %0.2f %0.2f %5.2f %9.2f %9.2f' % \
                           (host, load_id, x, y, z, stress,
                            float(info_pro['time']['real']), 
                            load_compute, 
                            info_pro['cpu']['utilization'], 
                            info_pro['cpu']['efficiency'], 
                            info_pro['sys']['load'],
                            load_memory, 
                            load_storage
                           )
                print output
                             
                iter_1_time .append(float(info_pro['time']['real']))
                iter_1_cpu  .append(float(load_compute))
                iter_1_mem  .append(float(load_memory))
                iter_1_io   .append(float(load_storage))
                iter_1_util .append(float(info_pro['cpu']['utilization']))
                iter_1_eff  .append(float(info_pro['cpu']['efficiency']))
                iter_1_sys  .append(float(info_pro['sys']['load']))
    
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
            
            load_id  = 'MEAN_PRO.%04d' % x
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
    
            load_id  = 'STD_PRO.%04d' % x
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
    
            load_id  = 'STAT_PRO.%04d' % x
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
    
            # --------------------------------------------------------------------------------------------
           
            iter_2_time = list()
            iter_2_tcpu = list()
            iter_2_tmem = list()
            iter_2_tio  = list()
            iter_2_cpu  = list()
            iter_2_mem  = list()
            iter_2_io   = list()
            iter_2_util = list()
            iter_2_eff  = list()
            iter_2_sys  = list()

            iter_1_mean_cpu = 92881.19
            iter_1_mean_mem =  2016.00
            iter_1_mean_io  =  1437.55
    
            for iter in range (iters) :
    
                info_s, ret, out = rs.profile (synaptic, x, y, z,
                        iter_1_mean_cpu, iter_1_mean_mem, iter_1_mean_io)
    
              # print "#####################"
              # pp.pprint (ret['m'])
              # print "#####################"
    
                load_compute = float(info_s['cpu']['ops' ]) / (1024*1024) / 8
                load_memory  = float(ret['m']['ru.maxrss']) / (1024*1024)
                load_storage = float(info_s['io']['write']) / (1024*1024)
           
                load_id  = 'EMU.%04d' % x
                output   = '%-10s %15s %5d %5d %5d %5d %9.2f %9.2f %9.2f %9.2f %9.2f %0.2f %0.2f %5.2f %9.2f %9.2f' % \
                           (host, load_id, x, y, z, stress, 
                            float(info_s['time']['real']), 
                            ret['c']['timer'], 
                            ret['m']['timer'], 
                            ret['s']['timer'],
                            load_compute, 
                            info_s['cpu']['utilization'], 
                            info_s['cpu']['efficiency'], 
                            info_s['sys']['load'],
                            load_memory, 
                            load_storage
                            )
                print output
    
                iter_2_time .append(float(info_s['time']['real']))
                iter_2_tcpu .append(float(ret['c']['timer']))
                iter_2_tmem .append(float(ret['m']['timer']))
                iter_2_tio  .append(float(ret['s']['timer']))
                iter_2_cpu  .append(float(load_compute))
                iter_2_mem  .append(float(load_memory))
                iter_2_io   .append(float(load_storage))
                iter_2_util .append(float(info_s['cpu']['utilization']))
                iter_2_eff  .append(float(info_s['cpu']['efficiency']))
                iter_2_sys  .append(float(info_s['sys']['load']))
    
            iter_2_mean_time = numpy.mean (numpy.array (iter_2_time))
            iter_2_mean_tcpu = numpy.mean (numpy.array (iter_2_tcpu))
            iter_2_mean_tmem = numpy.mean (numpy.array (iter_2_tmem))
            iter_2_mean_tio  = numpy.mean (numpy.array (iter_2_tio ))
            iter_2_mean_cpu  = numpy.mean (numpy.array (iter_2_cpu ))
            iter_2_mean_mem  = numpy.mean (numpy.array (iter_2_mem ))
            iter_2_mean_io   = numpy.mean (numpy.array (iter_2_io  ))
            iter_2_mean_util = numpy.mean (numpy.array (iter_2_util))
            iter_2_mean_eff  = numpy.mean (numpy.array (iter_2_eff ))
            iter_2_mean_sys  = numpy.mean (numpy.array (iter_2_sys ))
    
            iter_2_std_time  = numpy.std  (numpy.array (iter_2_time))
            iter_2_std_tcpu  = numpy.std  (numpy.array (iter_2_tcpu))
            iter_2_std_tmem  = numpy.std  (numpy.array (iter_2_tmem))
            iter_2_std_tio   = numpy.std  (numpy.array (iter_2_tio ))
            iter_2_std_cpu   = numpy.std  (numpy.array (iter_2_cpu ))
            iter_2_std_mem   = numpy.std  (numpy.array (iter_2_mem ))
            iter_2_std_io    = numpy.std  (numpy.array (iter_2_io  ))
            iter_2_std_util  = numpy.std  (numpy.array (iter_2_util))
            iter_2_std_eff   = numpy.std  (numpy.array (iter_2_eff ))
            iter_2_std_sys   = numpy.std  (numpy.array (iter_2_sys ))
            
            load_id  = 'MEAN_EMU.%04d' % x
            mean     = '%-10s %15s %5d %5d %5d %5d %9.2f %9.2f %9.2f %9.2f %9.2f %.2f %.2f %5.2f %9.2f %9.2f' % \
                       (host, load_id, x, y, z, stress, 
                        iter_2_mean_time, 
                        iter_2_mean_tcpu, 
                        iter_2_mean_tmem,
                        iter_2_mean_tio, 
                        iter_2_mean_cpu,
                        iter_2_mean_util, 
                        iter_2_mean_eff, 
                        iter_2_mean_sys,
                        iter_2_mean_mem, 
                        iter_2_mean_io
                       )
            print mean  
    
            load_id  = 'STD_EMU.%04d' % x
            std      = '%-10s %15s %5d %5d %5d %5d %9.2f %9.2f %9.2f %9.2f %9.2f %.2f %.2f %5.2f %9.2f %9.2f' % \
                       (host, load_id, x, y, z, stress, 
                        iter_2_std_time, 
                        iter_2_std_tcpu,
                        iter_2_std_tmem,
                        iter_2_std_tio,
                        iter_2_std_cpu,
                        iter_2_std_util, 
                        iter_2_std_eff, 
                        iter_2_std_sys,
                        iter_2_std_mem, 
                        iter_2_std_io
                       )
            print std
    
            load_id  = 'STAT_EMU.%04d' % x
            stat     = '%-10s %15s %5d %5d %5d %5d %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %9.2f %.2f %.2f %.2f %.2f %5.2f %5.2f %9.2f %9.2f %9.2f %9.2f' % \
                       (host, load_id, x, y, z, stress, 
                        iter_2_mean_time, 
                        iter_2_std_time, 
                        iter_2_mean_tcpu,
                        iter_2_std_tcpu,
                        iter_2_mean_tmem,
                        iter_2_std_tmem,
                        iter_2_mean_tio,
                        iter_2_std_tio,
                        iter_2_mean_cpu,
                        iter_2_std_cpu,
                        iter_2_mean_util, 
                        iter_2_std_util, 
                        iter_2_mean_eff, 
                        iter_2_std_eff, 
                        iter_2_mean_sys,
                        iter_2_std_sys,
                        iter_2_mean_mem, 
                        iter_2_std_mem, 
                        iter_2_mean_io,
                        iter_2_std_io
                       )
            print stat  
    
    
          # print ' ---------------------------------------------------------------'
          # print " MB  %-25s : %15.2f s" % ('time.real',               float(info_pro['time']['real'         ]))
          # print " MB  %-25s : %15.2f"   % ('sys.load',                float(info_pro['sys']['load'          ]))
          # print " MB  %-25s : %s"       % ('cpu.ops',            n2h (float(info_pro['cpu']['ops'           ]), rs.PREFIX_ISO, 'FLOP'  , "%(val)15.2f %(unit)s"))
          # print " MB  %-25s : %s"       % ('cpu.utilization',    n2h (float(info_pro['cpu']['utilization'   ]), rs.PREFIX_ISO, ''      , "%(val)15.2f %(unit)s"))
          # print " MB  %-25s : %s"       % ('cpu.efficiency',     n2h (float(info_pro['cpu']['efficiency'    ]), rs.PREFIX_ISO, ''      , "%(val)15.2f %(unit)s"))
          # print " MB  %-25s : %s"       % ('cpu.flops_per_core', n2h (float(info_pro['cpu']['flops_per_core']), rs.PREFIX_ISO, 'FLOP/s', "%(val)15.2f %(unit)s"))
          # print " MB  %-25s : %s"       % ('io.write',           n2h (float(info_pro['io']['write'          ]), rs.PREFIX_BIN, 'Byte'  , "%(val)15.2f %(unit)s"))
          # print " MB  %-25s : %s"       % ('mem.peak',           n2h (float(info_pro['mem']['peak'          ]), rs.PREFIX_BIN, 'Byte'  , "%(val)15.2f %(unit)s"))
          # print ' ---------------------------------------------------------------'                                                        
          # print " SYN %-25s : %15.2f s" % ('time.real',               float(info_s['time']['real'         ]))                            
          # print " SYN %-25s : %15.2f"   % ('sys.load',                float(info_s['sys']['load'          ]))
          # print " SYN %-25s : %s"       % ('cpu.ops',            n2h (float(info_s['cpu']['ops'           ]), rs.PREFIX_ISO, 'FLOP'  , "%(val)15.2f %(unit)s"))
          # print " SYN %-25s : %s"       % ('cpu.utilization',    n2h (float(info_s['cpu']['utilization'   ]), rs.PREFIX_ISO, ''      , "%(val)15.2f %(unit)s"))
          # print " SYN %-25s : %s"       % ('cpu.efficiency',     n2h (float(info_s['cpu']['efficiency'    ]), rs.PREFIX_ISO, ''      , "%(val)15.2f %(unit)s"))
          # print " SYN %-25s : %s"       % ('cpu.flops_per_core', n2h (float(info_s['cpu']['flops_per_core']), rs.PREFIX_ISO, 'FLOP/s', "%(val)15.2f %(unit)s"))
          # print " SYN %-25s : %s"       % ('io.write',           n2h (float(info_s['io']['write'          ]), rs.PREFIX_BIN, 'Byte'  , "%(val)15.2f %(unit)s"))
          # print " SYN %-25s : %s"       % ('mem.peak',           n2h (float(info_s['mem']['peak'          ]), rs.PREFIX_BIN, 'Byte'  , "%(val)15.2f %(unit)s"))
          # print ' ---------------------------------------------------------------'
          # pp.pprint (info_pro)                                  
          # print ' ---------------------------------------------------------------'
          # pp.pprint (info_s)                                  
          # print ' ---------------------------------------------------------------'
          # pp.pprint (ret)                                  
          # print ' ---------------------------------------------------------------'
    
            print

            # --------------------------------------------------------------------------------------------

            if  stress :
                stresser.terminate ()
                time.sleep (1)
                stresser.kill ()

                sp.call ("killall    stress", shell=True)
                sp.call ("killall -9 stress", shell=True)

