#!/usr/bin/env python


import os
import sys
import math
import time
import pymongo
from   PIL import Image

import radical.utils as ru

# ------------------------------------------------------------------------------
#
def usage (msg=None) :
    """
    print usage.  If message is given, we exit with that error message
    otherwise we exit peacefully .
    """

    if  msg :
        sys.stderr.write ('\n    Error: %s' % msg)

    print """

    usage :

        python mandelbrot_master.py
               --master_id=mongodb://host.net:port/path
               --num_workers=4
               --mb_size=1024
               --mb_depth=128

        or

        python mandelbrot_master.py
               -i=mongodb://host.net:port/path
               -n=4
               -s=1024
               -d=1024

        ID is mandatory.
    """

    if  msg :
        sys.exit (1)

    else :
        sys.exit (0)


# ------------------------------------------------------------------------------
#
def main (master_id, num_workers, mb_size, mb_depth) :

    [host, port, dbname, cname, _, _, _] = ru.split_dburl (master_id)

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]
    collection = database[cname]

  # collection.remove ()
  
    subsx   = int(math.sqrt(num_workers))
    subsy   = int(math.sqrt(num_workers))
    
    minx    = -2.0
    maxx    =  1.0
    miny    = -1.5
    maxy    =  1.5
    pixx    =  mb_size  # divisible by subsx
    pixy    =  mb_size  # divisible by subsy
    iters   =  mb_depth
    image   =  Image.new ("RGB", (pixx, pixy))
    
    stepx   = (maxx-minx) / subsx
    stepy   = (maxy-miny) / subsy
    
    spixx   =  pixx / subsx
    spixy   =  pixy / subsy

    # initialize white pic
    for     x in range (0, pixx) :
        for y in range (0, pixy) :
            image.putpixel ((x, y), (255, 255, 255))
    image.save  ("%s/mandel.png" % os.environ['HOME'], "PNG")


    workers = dict()
    
    # subdivide and publish work items
    for   subx in range (0, subsx) :
      for suby in range (0, subsy) :
    
          worker_idx = subx * subsx + suby
          worker_doc = {'worker_id' : int(worker_idx), 
                        'type'      : 'work',
                        'minx'      : float(minx + subx * stepx),
                        'miny'      : float(miny + suby * stepy),
                        'maxx'      : float(minx + subx * stepx + stepx),
                        'maxy'      : float(miny + suby * stepy + stepy),
                        'pixx'      : spixx,
                        'pixy'      : spixy,
                        'subx'      : subx,
                        'suby'      : suby,
                        'iters'     : int(iters)
                        }
  
          workers[worker_idx] = worker_doc
  
          collection.insert (workers[worker_idx])


    # wait for and evaluate results
    done    = list()

    while len(done) != len(workers) :

        print "waiting (%s/%s)" % (len(done), len(workers))

        results = collection.find ({'type' : 'result'})
        active  = False

        for result in results :

            worker_id = result['worker_id']
            pixx      = result['pixx']
            pixy      = result['pixy']
            subx      = result['subx']
            suby      = result['suby']

            if  worker_id not in done :

                active = True
                data   = result['data']

                for     x in range (0, pixx) :
                    for y in range (0, pixy) :
                        i = data[x][y]
                        image.putpixel ((spixx*subx+y, spixy*suby+x), (i/4, i/4, i))

                done.append (worker_id)
                image.save  ("%s/mandel.png" % os.environ['HOME'], "PNG")

        if  not active:
            time.sleep (1)

    print "done    (%s/%s)" % (len(done), len(workers))

    db_client.disconnect ()



# ------------------------------------------------------------------------------
#
if __name__ == '__main__' :

    """
    parse arguments, and trigger action workload.
    """

    master_id   = None
    num_workers = 1
    mb_size     = 1024
    mb_depth    = 1024

    for arg in sys.argv[1:] :

        if  arg == '--help' :
            usage ()

        else :
            if  not '=' in arg :
                usage ("invalid argument '%s'" % arg)

            key, val = arg.split ('=', 1)

            if  key == '--master_id' or \
                key == '-i'          :
                master_id = val

            elif key == '--num_workers' or \
                 key == '-n'            :
                num_workers = int(val)

            elif key == '--mb_size' or \
                 key == '-s'        :
                mb_size = int(val)

            elif key == '--mb_depth' or \
                 key == '-d'         :
                mb_depth = int(val)

            else :
                usage ("parameter '%s' not supported" % arg)


    if  not master_id :
        usage ("need master_id to operate (%s)" % sys.argv)

    main (master_id, num_workers, mb_size, mb_depth)
    

