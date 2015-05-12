

import os
import time
import signal
import pprint
import pymongo
import radical.utils        as ru
import radical.utils.logger as rul

# import pudb 
# pudb.set_interrupt_handler ()


_DEFAULT_DBURL = 'mongodb://localhost:27017/synapse_v0_5'
PROFILE_DBURL  = os.environ.get ('RADICAL_SYNAPSE_DBURL', _DEFAULT_DBURL)

LOAD        = int (os.environ.get ('RADICAL_SYNAPSE_LOAD', '0'))
LOAD_CMD    = "top -b -n1 | head -1  |       cut -f 4 -d :         | cut -f 1 -d ,"
LOAD_CMD    = "top -b -n1 | head -n1 | rev | cut -f 3 -d \  | rev  | sed -e 's/,//'"


# ------------------------------------------------------------------------------
#
logger = rul.getLogger  ('radical.synapse')


# ------------------------------------------------------------------------------
#
_stamp_zero = None
def timestamp():
    global _stamp_zero
    if not _stamp_zero :
        _stamp_zero = time.time()
        return 0.0
    return time.time() - _stamp_zero

def time_zero():
    return _stamp_zero


# ------------------------------------------------------------------------------
#
#
PREFIX_BIN = { 'K' : 1024,
               'M' : 1024 * 1024,
               'G' : 1024 * 1024 * 1024,
               'T' : 1024 * 1024 * 1024 * 1024,
               'P' : 1024 * 1024 * 1024 * 1024 * 1024,
               'E' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024,
               'Z' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024,
               'Y' : 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
             }

PREFIX_ISO = { 'K' : 1000,
               'M' : 1000 * 1000,
               'G' : 1000 * 1000 * 1000,
               'T' : 1000 * 1000 * 1000 * 1000,
               'P' : 1000 * 1000 * 1000 * 1000 * 1000,
               'E' : 1000 * 1000 * 1000 * 1000 * 1000 * 1000,
               'Z' : 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000,
               'Y' : 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
             }


# ------------------------------------------------------------------------------
#
def human_to_number (h, prefix=PREFIX_BIN) :

    rs = ru.ReString (h)

    with rs // '^\s*([\d\.]+)\s*(\D+)\s*$' as match : 
        if  not match :
          # print 'incorrect format: %s' % h
            return float(h)

        p = match[1].upper()[0]

        if  not p in prefix :
          # print 'unknown prefix: %s' % h
            return float(h)

        return float(match[0]) * prefix[p]


# ------------------------------------------------------------------------------
#
def number_to_human (n, prefix=PREFIX_BIN, unit='', template="%(val)f %(unit)s") :

    for key in prefix.keys () :

        hn = n / float(prefix[key])
        if  hn > 1 and hn < 1000 :
            return template % {'val' : hn, 'unit' : "%s%s" % (key, unit)}

    return template % {'val' : n, 'unit' : unit}


# ------------------------------------------------------------------------------
#
def time_to_seconds (t) :

    rs = ru.ReString (t)

    with rs // '^(?:\s*(\d+)\s*[:])+\s*([\d\.]+)\s*$' as match :

        if  not match :
            return t

        seconds = 0
        if  len(match) ==  1 : seconds = float(match[0])
        if  len(match) ==  2 : seconds = float(match[0]) * 60      + float(match[1])
        if  len(match) ==  3 : seconds = float(match[0]) * 60 * 60 + float(match[1]) * 60 + float(match[2])

        return seconds


# ------------------------------------------------------------------------------
def store_profile (command, info) :

    # FIXME: this should probably use find_and_modify.  Also, the index should
    # be a MongoDB index (to ensure uniqueness)

    command_idx = index_command (command)

    print 'dburl: %s' % PROFILE_DBURL

    [host, port, dbname, _, _, _, _] = ru.split_dburl (PROFILE_DBURL)

  # print 'url       : %s' % PROFILE_DBURL
  # print 'host      : %s' % host
  # print 'port      : %s' % port
  # print 'database  : %s' % dbname

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]
    collection = database['profiles']

    results    = collection.find ({'type'        : 'profile', 
                                   'command_idx' : command_idx})

    if  results.count() :
        # expand existing profile
        profile = results[0]
    else:
        # create new profile
        profile = {'type'        : 'profile', 
                   'command_idx' : command_idx, 
                   'profiles'    : list()}


    profile['profiles'].append (info)

    collection.save (profile)
  # print 'profile stored in %s' % [host, port, dbname, 'profiles']


# ------------------------------------------------------------------------------
def get_profile (command) :

    command_idx = index_command (command)

    [host, port, dbname, _, _, _, _] = ru.split_dburl (PROFILE_DBURL)

  # print 'url       : %s' % PROFILE_DBURL
  # print 'host      : %s' % host
  # print 'port      : %s' % port
  # print 'database  : %s' % dbname

    db_client  = pymongo.MongoClient (host=host, port=port)
    database   = db_client[dbname]
    collection = database['profiles']

    results    = collection.find ({'type'    : 'profile', 
                                   'command' : command,
                                   'index'   : command_idx})

    if  not results.count() :
        raise RuntimeError ("Could not get profile for %s at %s/profiles" % (command, PROFILE_DBURL))


  # print 'profile retrieved from %s' % [host, port, dbname, 'profiles']
  # pprint.pprint (results[0])
    return results[0]


# ------------------------------------------------------------------------------
#
def index_command (command) :

    # for now, only index by executable name.  We assume that this is the first
    # element of the command -- but if that is a known interpreter, we use the
    # second element (assuming it is a script name)
    elems = command.split()

    if elems[0] in ['python', 'sh', 'bash', '/bin/sh', 'time'] :
        # return the first element which is not an option
        for elem in elems[1:] :
            if not elem.startswith ('-') :
                return elem

    # all others, index by first element
    return elems[0]


# ------------------------------------------------------------------------------

