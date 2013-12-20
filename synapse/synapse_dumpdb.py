#!/usr/bin/env python


import sys
import pprint
import pymongo

import synapse
import synapse.utils as su

_DEFAULT_DBURL = 'mongodb://localhost:27017/'
_DEFAULT_DBURL = 'mongodb://ec2-184-72-89-141.compute-1.amazonaws.com:27017/'


# ------------------------------------------------------------------------------
#
def dump (url, mode) :
    """
    Connect to mongodb at the given location, and traverse the data bases
    """

    [host, port, dbname, cname, pname] = su.split_dburl (url)

    db_client  = pymongo.MongoClient (host=host, port=port)

    print 'host      : %s' % host
    print 'port      : %s' % port

 
    if  dbname : dbnames = [dbname]
    else       : dbnames = db_client.database_names ()

    for name in dbnames :

        if  mode == 'list' and not dbname :
            print " +-- db   %s" % name

        elif  mode == 'remove' :
            
            if (not dbname) or (name == dbname) :
                try :
                    db_client.drop_database (name)
                    print "  removed database %s" % name
                except :
                    pass # ignore system tables

        else :
            handle_db (db_client, mode, name, cname, pname)

    db_client.disconnect ()


# ------------------------------------------------------------------------------
def handle_db (db_client, mode, dbname, cname, pname) :
    """
    For the given db, traverse collections
    """

    database = db_client[dbname]
    print " +-- db   %s" % dbname


    if  cname : cnames = [cname]
    else      : cnames = database.collection_names ()

    for name in cnames :

        if  mode == 'list' and not cname :
            print " | +-- coll %s" % name

        elif  mode == 'remove' and not pname :
            try :
                database.drop_collection (name)
                print "  removed collection %s" % name
            except :
                pass # ignore errors

        else :
            handle_coll (database, mode, name, pname)



# ------------------------------------------------------------------------------
def handle_coll (database, mode, cname, pname) :
    """
    For a given collection, traverse all documents
    """

    if 'indexes' in cname :
        return

    collection = database[cname]
    print " | +-- coll %s" % cname

    docs = collection.find ()

    for doc in docs :

        name = doc['_id']

        if  mode == 'list' and not pname :
            print " | | +-- doc  %s" % name

        elif  mode == 'remove' :
            if (not pname) or (str(name)==str(pname)) :
                try :
                    collection.remove (name)
                    print "  removed document %s" % name
                except Exception as e:
                    pass # ignore errors

        else :
            if (not pname) or (str(name)==str(pname)) :
                handle_doc (collection, mode, doc)


# ------------------------------------------------------------------------------
def handle_doc (collection, mode, doc) :
    """
    And, surprise, for a given document, show it according to 'mode'
    """

    name = doc['_id']

    if  mode == 'list' :

        for key in doc :
            print " | | | +-- %s" % (key)

    elif  mode == 'tree' :
        print " | | +-- doc  %s" % (name)
        for key in doc :
            print " | | | +-- %s" % (key)

    elif  mode == 'dump' :
        print " | | +-- doc  %s" % (name)
        for key in doc :
            print " | | | +-- %-10s : %s" % (key, doc[key])


# ------------------------------------------------------------------------------
#
if __name__ == '__main__' :

    if  len(sys.argv) == 3 :
        mode = sys.argv[1]
        url  = sys.argv[2]
    
    elif len(sys.argv) == 2 :
        mode = 'tree'
        url  = sys.argv[1]

    elif len(sys.argv) == 1 :
        mode = 'tree'
        url  = _DEFAULT_DBURL

    else :
        print """

      usage   : %s [command] <url>
      example : %s remove mongodb://localhost:27017//synapse_profiles/profiles/

      The URL is interpreted as:
          [schema]://[host]:[port]/[database]/[collection]/[path]

      Path is at the moment not evaluated.  Commands are:

        tree:   show a tree of the hierarchy, but only  document IDs, no content
        dump:   show a tree of the hierarchy, including document contents
        list:   list entries in the subtree, but do not traverse
        remove: remove the specified subtree

      The default command is 'tree'.

"""
        sys.exit (0)

    dump (url, mode)


