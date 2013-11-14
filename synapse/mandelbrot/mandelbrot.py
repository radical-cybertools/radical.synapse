
import os
import sys
import time
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
    app = dict()
    app['c'] = sa.Compute ()
    app['m'] = sa.Memory  ()
    app['s'] = sa.Storage ()

    # the atoms below are executed concurrently (in their own threads)
    app['c'].run (info={'n'   : load_compute})
    app['m'].run (info={'n'   : load_memory})
    app['s'].run (info={'n'   : load_storage,
                            'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})

    # all are started -- now wait for completion and collect times
    times = {}
    times['c'] = 0.0
    times['m'] = 0.0
    times['s'] = 0.0

    info_c = app['c'].wait ()
    info_m = app['m'].wait ()
    info_s = app['s'].wait ()

    t_c    = float(info_c['timer'])
    t_m    = float(info_m['timer'])
    t_s    = float(info_s['timer'])

    times['c'] += t_c
    times['m'] += t_m
    times['s'] += t_s

    output = '%-10s %10s    %7.2f %7.2f %7.2f %7.2f %5d %5d %5d %5d %5d %5d %5d' % \
            (host, load_id, time.time() - start, t_c, t_m, t_s,
             load_instances, load_compute, load_memory, load_storage, x, y, z)

    return [t_c, t_m, t_s]


# ------------------------------------------------------------------------------
#

for xy in [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120] :
    for z in [250] : 
        # print "%d %d %d" % (xy, xy, z)

# # ------------------------------------------------------------------------------
#         pass
# if True :
#     if True :
#         xy = 1000
#         z  = 1
# # ------------------------------------------------------------------------------

        _, info_1 = su.benchmark_function (mandel, xy, xy, z)

        load_compute = int(float(info_1['cpu.ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_1['mem.peak']) / (1024*1024))
        load_storage = int(float(info_1['io.write']) / (1024*1024))

        load_id  = 'RMB.%04d' % xy
        output   = '%-10s %10s    %7.2f ------- ------- ------- %5d %9d %9d %9d %5d %5d %5d %5.1f %5.1f' % \
                   (host, load_id, float(info_1['time.real']), 
                    1, load_compute, load_memory, load_storage,
                    xy, xy, z,
                    info_1['cpu.cycles idle front'], info_1['cpu.cycles idle back'])
        print output


        # --------------------------------------------------------------------------------------------
       
        load_compute = int(float(info_1['cpu.ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_1['mem.peak']) / (1024*1024))
        load_storage = int(float(info_1['io.write']) / (1024*1024))
       
        out, info_2 = su.benchmark_function (synaptic, xy, xy, z, load_compute, load_memory, load_storage)

        load_compute = int(float(info_2['cpu.ops' ]) / (1024*1024) / 8)
        load_memory  = int(float(info_2['mem.peak']) / (1024*1024))
        load_storage = int(float(info_2['io.write']) / (1024*1024))
       
        load_id  = 'SMB.%04d' % xy
        output   = '%-10s %10s    %7.2f %7.2f %7.2f %7.2f %9d %9d %9d %5d %5d %5d %5d %5.1f %5.1f' % \
                   (host, load_id, float(info_2['time.real']), 
                    out[0], out[1], out[2],
                    1, load_compute, load_memory, load_storage,
                    xy, xy, z,
                    info_2['cpu.cycles idle front'], info_2['cpu.cycles idle back'])

        print output

        

     #  print ' ---------------------------------------------'
     #  for key in ['time.real', 
     #              'cpu.ops', 
     #              'io.write', 
     #              'mem.peak'    ,
     #              'cpu.cycles idle front',
     #              'cpu.cycles idle back' ] :
     #      print " RMB %-25s : %15.1f" % (key, float(info_1[key]))
     #      print " SMB %-25s : %15.1f" % (key, float(info_2[key]))
     #  print ' ---------------------------------------------'

