#!/usr/bin/env python


import sys
import pprint
import pymongo

import synapse
import synapse.utils as su

DEFAULT_URL = '%s/synapse_profiles/profiles' % synapse.SYNAPSE_DBURL


# ------------------------------------------------------------------------------
#
def dump (master_id) :
    """
    Connect to mongodb at the given location, and dump all docs in the given
    collection.
    """

    [host, port, dbname, cname] = su.split_dburl (master_id)

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]

    print 'host      : %s' % host
    print 'port      : %s' % port
    print 'database  : %s' % dbname

    if  not cname :
        # just list collections
        print 'collections: %s' % database.collection_names ()

    elif cname in ['REMOVE', 'DROP'] :
        # remove all collections
        for collection in database.collection_names () :
            try :
                database.drop_collection (collection)
                print 'drop collection: %s' % collection
            except :
                # ignore errors on system collections
                pass

    else :
        print 'collection: %s' % cname
        collection = database[cname]
        docs = collection.find ()

        if  not docs.count() :
            print "no docs in collection"

        for doc in docs:
            pprint.pprint (doc)

        db_client.disconnect ()


# ------------------------------------------------------------------------------
#
if __name__ == '__main__' :

    if  len(sys.argv) < 2 :
        url = DEFAULT_URL
    else :
        url = sys.argv[1]

    dump (url)


