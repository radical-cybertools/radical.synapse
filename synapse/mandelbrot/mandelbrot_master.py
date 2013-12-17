
import os
import time
import pymongo
from   PIL import Image

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
def main (master_id) :

    [host, port, collection] = split_url (master_id)

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client['synapse_mandelbrot']
    collection = database[collection]

    collection.remove ()
  
    subsx   = 4
    subsy   = 4
    
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
                image.save ("mandel.png", "PNG")

        if  not active:
            time.sleep (1)

    print "done    (%s/%s)" % (len(done), len(workers))

    db_client.disconnect ()



# ------------------------------------------------------------------------------
#
if __name__ == '__main__' :

    if  not 'SYNAPSE_MB_MASTER' in os.environ :
        raise LookupError ("'SYNAPSE_MB_MASTER' not set in environment")

    main (os.environ['SYNAPSE_MB_MASTER'])


