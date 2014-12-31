#!/usr/bin/env python


import os
import sys
import time   
import pymongo

import radical.utils as ru

ATTEMPTS = 10

# ------------------------------------------------------------------------------
#
def work (master_id, worker_id) :
    """
    Connect to mongodb at the given location, grab a work item from it, invoke
    the mb calculation for the given region, and push the results back.

    The path element of the master_id (which is considered to be a URL) is used
    as collection ID, the client ID will specify the worker document.
    """


    [host, port, dbname, cname, _, _, _] = ru.split_dburl (master_id)
    [host, port, dbname, cname, _, _, _] = ru.split_dburl (master_id)

    print "  %s:%d" % (host, port)
    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]
    collection = database[cname]
    docs = collection.find ()

  # for i in db_client.database_names  () : print "  %s" % i
  # for i in database.collection_names () : print "     %s" % i
  # print "      %d docs" % docs.count()

    print 'master id : %s' % master_id
    print 'worker id : %s' % worker_id
    print 'host      : %s' % host
    print 'port      : %s' % port
    print 'dbname    : %s' % dbname
    print 'cname     : %s' % cname
    print 'worker_id : %s' % worker_id 
    print 'works     : %s' % collection.find ().count()

    attempts = 0

    while attempts < ATTEMPTS :
        work = collection.find_one ({'worker_id': int(worker_id),
                                     'type'     : 'work'})
        if  work :
            break
        else :
            print 'waiting for work'
            time.sleep (1)

    if  not work :
        print "cannot find work for %s : %s" % (master_id, worker_id)
        sys.exit (0) # silent exit


    print 'work      : %s' % str(work)

    result = mandelbrot_calc (work)

    print 'publish result'
    collection.insert (result)

    db_client.disconnect ()


# ------------------------------------------------------------------------------
#
def mandelbrot_calc (work) :
    """    
    compute the mandelbrot (sub)set with the given parameters.
    `work` is considered to be a dict with the following keys::

        xmin, ymin :  lower left corner in complex plane
        xmax, ymax :  upper right corner in complex plane
        xpix, ypix :  sub-picture resolution 
        iters      :  max iterations

    """

    start = time.time()

    if  'minx'  not in work : usage ("No 'minx'   in work '%s'" % work)
    if  'miny'  not in work : usage ("No 'miny'   in work '%s'" % work)
    if  'maxx'  not in work : usage ("No 'maxx'   in work '%s'" % work)
    if  'maxy'  not in work : usage ("No 'maxy'   in work '%s'" % work)
    if  'pixx'  not in work : usage ("No 'pixx'   in work '%s'" % work)
    if  'pixy'  not in work : usage ("No 'pixy'   in work '%s'" % work)
    if  'subx'  not in work : usage ("No 'subx'   in work '%s'" % work)
    if  'suby'  not in work : usage ("No 'suby'   in work '%s'" % work)
    if  'iters' not in work : usage ("No 'iters'  in work '%s'" % work)

    minx  = work['minx']
    miny  = work['miny']
    maxx  = work['maxx']
    maxy  = work['maxy']
    pixx  = work['pixx']
    pixy  = work['pixy']
    subx  = work['subx']
    suby  = work['suby']
    iters = work['iters']

  # print "minx  : %s " % minx
  # print "miny  : %s " % miny
  # print "maxx  : %s " % maxx
  # print "maxy  : %s " % maxy
  # print "pixx  : %s " % pixx
  # print "pixy  : %s " % pixy
  # print "subx  : %s " % subx
  # print "suby  : %s " % suby
  # print "iters : %s " % iters

    data = list()

    for y in range (0, pixy) :
    
        zy = y * (maxy - miny) / (pixy - 1) + miny

        line = list()
    
        for x in range (0, pixx) :
    
            zx = x * (maxx - minx) / (pixx - 1)  + minx
            z  = zx + zy * 1j
            c  = z
    
            for i in range (0, iters) :
                if  abs(z) > 2.0 :
                    break 
    
                z = z * z + c

            line.append (i)

        data.append (line)


    result = {'worker_id' : int(worker_id), 
              'type'      : 'result' ,
              'pixx'      : pixx, 
              'pixy'      : pixy, 
              'subx'      : subx, 
              'suby'      : suby, 
              'data'      : data, 
              'time'      : time.time()-start,
              'host'      : os.popen('hostname -f').read().strip()}

    return result


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

        python mandelbrot_worker.py
               --master_id=mongodb://host.net:port/path
               --worker_id=3

    """

    if  msg :
        sys.exit (1)

    else :
        sys.exit (0)


# ------------------------------------------------------------------------------
#
if __name__ == '__main__' :
    """
    parse arguments, and trigger workload.
    This slave is basically stateless: it either works or does not.  It will
    grab a *single* work item from  mongodb and calculate the mb subset
    specified within, and then will store the result back at the same location,
    and exits.

    """

    master_id = None
    worker_id = None

    for arg in sys.argv[1:] :

        if  arg == '--help' :
            usage ()

        else :
            if  not '=' in arg :
                usage ("invalid argument '%s'" % arg)

            key, val = arg.split ('=', 1)

            if  key == '--master_id' :
                master_id = val

            elif key == '--worker_id' :
                worker_id = val

            else :
                # ignore other parameters, those are used for profile indexing
                pass
              # usage ("parameter '%s' not supported" % arg)


    if  not master_id or not worker_id :
        usage ("need master_id and worker_id to operate (%s)" % sys.argv)

    
    work (master_id, worker_id)

    sys.exit (0)


# ------------------------------------------------------------------------------

