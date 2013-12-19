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

    [host, port, dbname, cname, pname] = su.split_dburl (master_id)

    db_client  = pymongo.MongoClient (host=host, port=port)

    print 'host      : %s' % host
    print 'port      : %s' % port

    if  not dbname :
        print 'databases :'

        for dbname in db_client.database_names () :
            print "  %s" % dbname


    else :

        print 'database  : %s' % dbname
        database   = db_client[dbname]

        if  not cname :
            # just list collections
            print 'collections: '
            for cname in database.collection_names () :
                print "   %s" % cname


        else :

            if  cname in ['REMOVE', 'DROP'] :
                print "drop db %s" % dbname
                db_client.drop_database (dbname)
            else :

                print 'collection: %s' % cname
                collection = database[cname]

                if  pname in ['REMOVE', 'DROP'] :
                    print "remove collection %s" % cname
                    database.drop_collection (cname)

                else :

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


