#!/usr/bin/env python


import os
import sys
import math
import time
import pymongo
from   PIL import Image


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
               --num_wrokers=4

    """

    if  msg :
        sys.exit (1)

    else :
        sys.exit (0)


# ------------------------------------------------------------------------------
#
def split_url (url) :
    """
    we split the master_id, which is a URL, into the base mongodb URL, and the
    path element, which we use as collection id.
    """

    slashes = [idx for [idx,elem] in enumerate(url) if elem == '/']

    if  len(slashes) < 3 :
        usage ("master_id needs to be a mongodb URL, the path element must" \
               "specify the master's collection id")

    if  url[:slashes[0]].lower() != 'mongodb:' :
        usage ("master_id must be a 'mongodb://' url, not %s" % url)

    if  len(url) <= slashes[2]+1 :
        usage ("master_id needs to be a mongodb URL, the path element must" \
               "specify the master's collection id")

    base_url   = url[slashes[1]+1:slashes[2]]
    collection = url[slashes[2]+1:]

    if  ':' in base_url :
        host, port = base_url.split (':', 1)
        port = int(port)
    else :
        host, port = base_url, None

    return [host, port, collection]


# ------------------------------------------------------------------------------
#
def main (master_id, num_workers) :

    [host, port, collection] = split_url (master_id)

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client['synapse_mandelbrot']
    collection = database[collection]

    collection.remove ()
  
    subsx   = int(math.sqrt(num_workers))
    subsy   = int(math.sqrt(num_workers))
    
    minx    = -2.0
    maxx    =  1.0
    miny    = -1.5
    maxy    =  1.5
    pixx    =  1024  # divisible by subsx
    pixy    =  1024  # divisible by subsy
    iters   =  100
    image   =  Image.new ("RGB", (pixx, pixy))
    
    stepx   = (maxx-minx) / subsx
    stepy   = (maxy-miny) / subsy
    
    spixx   =  1024 / subsx
    spixy   =  1024 / subsy

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
    results = collection.find ({'type' : 'result'})
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

                for     y in range (0, pixy) :
                    for x in range (0, pixx) :
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

    for arg in sys.argv[1:] :

        if  arg == '--help' :
            usage ()

        else :
            if  not '=' in arg :
                usage ("invalid argument '%s'" % arg)

            key, val = arg.split ('=', 1)

            if  key == '--master_id' :
                master_id = val

            elif key == '--num_workers' :
                num_workers = int(val)

            else :
                usage ("parameter '%s' not supported" % arg)


    if  not master_id :
        usage ("need master_id to operate (%s)" % sys.argv)

    main (master_id, num_workers)
    

