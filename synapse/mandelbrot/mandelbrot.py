
import os
import time
import synapse.utils as su

# ------------------------------------------------------------------------------
#
def mandel () :

    x_pixels  = 1800
    y_pixels  = 1800
    x_min     = -2.0
    x_max     = +1.0
    y_min     = -1.5
    y_max     = +1.5
    iter_max  = 1
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
perf_info = su.benchmark_function (mandel)

for key in sorted (perf_info.iterkeys()) :
    print " %-25s : %15.1f" % (key, float(perf_info[key]))

