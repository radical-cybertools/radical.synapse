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

# for xy in [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240] :
for xy in [1024] :
    for z in [250] : 
        print "%d %d %d" % (xy, xy, z)

# # ------------------------------------------------------------------------------
#         pass
# if True :
#     if True :
#         xy = 1000
#         z  = 1
# # ------------------------------------------------------------------------------

        _, info_m = su.profile_function (mandel, xy, xy, z)

        load_compute = int(float(info_m['cpu.ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_m['mem.peak']) / (1024*1024))
        load_storage = int(float(info_m['io.write']) / (1024*1024))

        load_id  = 'RMB.%04d' % xy
        output   = '%-10s %10s    %7.2f ------- ------- ------- %5d %9d %9d %9d %5d %5d %5d %5.1f %5.1f' % \
                   (host, load_id, float(info_m['time.real']), 
                    1, load_compute, load_memory, load_storage,
                    xy, xy, z,
                    info_m['cpu.cycles idle front'], info_m['cpu.cycles idle back'])
        print output


        # --------------------------------------------------------------------------------------------
       
        load_compute = int(float(info_m['cpu.ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_m['mem.peak']) / (1024*1024))
        load_storage = int(float(info_m['io.write']) / (1024*1024))
       
        info_s, info_2 = su.profile_function (synaptic, xy, xy, z, load_compute, load_memory, load_storage)

        info_s.update (info_2)

        pp.pprint (info_s)
        load_memory = int( float(info_s['c']['ru.maxrss']) \
                         + float(info_s['m']['ru.maxrss']) \
                         + float(info_s['s']['ru.maxrss']) ) / (1024*1024)

        load_compute = int(float(info_s['cpu.ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_s['mem.peak']) / (1024*1024))
        load_storage = int(float(info_s['io.write']) / (1024*1024))
       
        load_id  = 'SMB.%04d' % xy
        output   = '%-10s %10s    %7.2f %7.2f %7.2f %7.2f %5d %9d %9d %9d %5d %5d %5d %5.1f %5.1f' % \
                   (host, load_id, float(info_s['time.real']), 
                    info_s['c']['timer'], info_s['m']['timer'], info_s['s']['timer'],
                    1, load_compute, load_memory, load_storage,
                    xy, xy, z,
                    info_s['cpu.cycles idle front'], info_s['cpu.cycles idle back'])

        print output

        

        print ' ---------------------------------------------'
        for key in ['time.real', 
                    'cpu.ops', 
                    'io.write', 
                    'mem.peak',
                    'mem.max',
                    'cpu.cycles idle front',
                    'cpu.cycles idle back' ] :
            print " RMB %-25s : %15.1f" % (key, float(info_m[key]))
            print " SMB %-25s : %15.1f" % (key, float(info_2[key]))
        print ' ---------------------------------------------'
        pp.pprint (info_m)
        print ' ---------------------------------------------'
        pp.pprint (info_2)
        print ' ---------------------------------------------'

