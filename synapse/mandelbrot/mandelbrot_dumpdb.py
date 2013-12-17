#!/usr/bin/env python


import os
import pymongo


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
def dump (master_id) :
    """
    Connect to mongodb at the given location, and dump all docs in the given
    collection.
    """

    [host, port, cname] = split_url (master_id)

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client['synapse_mandelbrot']
    collection = database[cname]

    print 'host      : %s' % host
    print 'port      : %s' % port
    print 'collection: %s' % cname

    docs = collection.find ()

    if  not docs.count() :
        print "no docs in collection"

    for doc in docs:
        print doc

    db_client.disconnect ()


# ------------------------------------------------------------------------------
#
if __name__ == '__main__' :

    if  not 'SYNAPSE_MB_MASTER' in os.environ :
        raise LookupError ("'SYNAPSE_MB_MASTER' not set in environment")

    dump (os.environ['SYNAPSE_MB_MASTER'])


