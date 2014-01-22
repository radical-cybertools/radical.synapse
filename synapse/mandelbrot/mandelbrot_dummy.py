#!/usr/bin/env python


import os
import sys
import time
import pprint        as pp
import radical.utils as ru
import synapse.utils as su
import synapse.atoms as sa


host  = os.getenv ('HOST', os.popen ('hostname | cut -f 1 -d . | xargs echo -n').read ())

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
    rgb_image = []

    for x in range (x_pixels) :

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


# ------------------------------------------------------------------------------
#
def synaptic (x, y, z, load_compute, load_memory, load_storage) :

    load_instances = 1
    load_id        = 'SMB.%04d' % x

  # print 'synaptic: %s %s %s' % (x, y, z)
  # print      '%8s: %s %s %s' % (load_id, load_compute, load_memory, load_storage)

    start = time.time()

    # create containers for different system workload types
    atoms = dict()
    atoms['c'] = sa.Compute ()
    atoms['m'] = sa.Memory  ()
    atoms['s'] = sa.Storage ()

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

n2h = su.number_to_human

# for xy in [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240] :
for xy in [1024] :
    for z in [250] : 
      # print "%d %d %d" % (xy, xy, z)

# # ------------------------------------------------------------------------------
#         pass
# if True :
#     if True :
#         xy = 1000
#         z  = 1
# # ------------------------------------------------------------------------------

        info_m, ret, out = su.profile_function (mandel, xy, xy, z)

        load_compute = int(float(info_m['cpu']['ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_m['mem']['max'])  / (1024*1024))
        load_storage = int(float(info_m['io']['write']) / (1024*1024))

        load_id  = 'RMB.%04d' % xy
        output   = '%-10s %10s    %7.2f ------- ------- ------- %5d %9d/%0.2f/%0.2f %9d %9d %5d %5d %5d %7.2f' % \
                   (host, load_id, float(info_m['time']['real']), 
                    1, load_compute, info_m['cpu']['utilization'], info_m['cpu']['efficiency'],
                    load_memory, load_storage,
                    xy, xy, z,
                    info_m['cpu']['efficiency'])
        print output


        # --------------------------------------------------------------------------------------------
       
        load_compute = int(float(info_m['cpu']['ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_m['mem']['max'])  / (1024*1024))
        load_storage = int(float(info_m['io']['write']) / (1024*1024))
       
        info_s, ret, out = su.profile_function (synaptic, xy, xy, z, load_compute, load_memory, load_storage)


        load_compute = int(float(info_s['cpu']['ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_s['mem']['max' ]) / (1024*1024))
        load_storage = int(float(info_s['io']['write']) / (1024*1024))
       
        load_id  = 'SMB.%04d' % xy
        output   = '%-10s %10s    %7.2f %7.2f %7.2f %7.2f %5d %9d/%0.2f/%0.2f %9d %9d %5d %5d %5d' % \
                   (host, load_id, float(info_s['time']['real']), 
                    0.0, 0.0, 0.0,
                    1, load_compute, info_s['cpu']['utilization'], info_s['cpu']['efficiency'],
                    load_memory, load_storage,
                    xy, xy, z)

        print output

        

      # print ' ---------------------------------------------------------------'
      # print " MB  %-25s : %15.2f s" % ('time.real',               float(info_m['time']['real'         ]))
      # print " MB  %-25s : %s"       % ('cpu.ops',            n2h (float(info_m['cpu']['ops'           ]), su.PREFIX_ISO, 'FLOP'  , "%(val)15.2f %(unit)s"))
      # print " MB  %-25s : %s"       % ('cpu.utilization',    n2h (float(info_m['cpu']['utilization'   ]), su.PREFIX_ISO, ''      , "%(val)15.2f %(unit)s"))
      # print " MB  %-25s : %s"       % ('cpu.efficiency',     n2h (float(info_m['cpu']['efficiency'    ]), su.PREFIX_ISO, ''      , "%(val)15.2f %(unit)s"))
      # print " MB  %-25s : %s"       % ('cpu.flops_per_core', n2h (float(info_m['cpu']['flops_per_core']), su.PREFIX_ISO, 'FLOP/s', "%(val)15.2f %(unit)s"))
      # print " MB  %-25s : %s"       % ('io.write',           n2h (float(info_m['io']['write'          ]), su.PREFIX_BIN, 'Byte'  , "%(val)15.2f %(unit)s"))
      # print " MB  %-25s : %s"       % ('mem.max',            n2h (float(info_m['mem']['max'           ]), su.PREFIX_BIN, 'Byte'  , "%(val)15.2f %(unit)s"))
      # print ' ---------------------------------------------------------------'                                                        
      # print " SYN %-25s : %15.2f s" % ('time.real',               float(info_s['time']['real'         ]))                            
      # print " SYN %-25s : %s"       % ('cpu.ops',            n2h (float(info_s['cpu']['ops'           ]), su.PREFIX_ISO, 'FLOP'  , "%(val)15.2f %(unit)s"))
      # print " SYN %-25s : %s"       % ('cpu.utilization',    n2h (float(info_s['cpu']['utilization'   ]), su.PREFIX_ISO, ''      , "%(val)15.2f %(unit)s"))
      # print " SYN %-25s : %s"       % ('cpu.efficiency',     n2h (float(info_s['cpu']['efficiency'    ]), su.PREFIX_ISO, ''      , "%(val)15.2f %(unit)s"))
      # print " SYN %-25s : %s"       % ('cpu.flops_per_core', n2h (float(info_s['cpu']['flops_per_core']), su.PREFIX_ISO, 'FLOP/s', "%(val)15.2f %(unit)s"))
      # print " SYN %-25s : %s"       % ('io.write',           n2h (float(info_s['io']['write'          ]), su.PREFIX_BIN, 'Byte'  , "%(val)15.2f %(unit)s"))
      # print " SYN %-25s : %s"       % ('mem.max',            n2h (float(info_s['mem']['max'           ]), su.PREFIX_BIN, 'Byte'  , "%(val)15.2f %(unit)s"))
      # print ' ---------------------------------------------------------------'
      # pp.pprint (info_m)                                  
      # print ' ---------------------------------------------------------------'
      # pp.pprint (info_s)                                  
      # print ' ---------------------------------------------------------------'

