

import os
import sys
import time
import glob
import signal
import pprint
import socket
import pymongo
import radical.utils        as ru

# import pudb
# pudb.set_interrupt_handler ()


LOAD = int (os.environ.get ('RADICAL_SYNAPSE_LOAD', '0'))

if 'darwin' not in sys.platform.lower():
  # LOAD_CMD    = "top -b -n1 | head -1  |       cut -f 4 -d :         | cut -f 1 -d ,"
    LOAD_CMD    = "top -b -n1 | head -n1 | rev | cut -f 3 -d \  | rev  | sed -e 's/,//'"
else:
    LOAD_CMD    = "top -l 1 | head -n 3 | tail -n 1 | cut -f 3 -d ' ' | cut -f 1 -d ','"


# ------------------------------------------------------------------------------
#
logger = ru.get_logger('radical.synapse')


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
def store_profile (profile, tags=None, url=None, mode=None) :

    if not url:
        url = os.environ.get ('RADICAL_SYNAPSE_DBURL')

    if not url:
        print "warning: need dburl to store profiles"
        return None

    if not mode:
        raise ValueError ("document needs mode (emulated | eecuted | profiled)")

    url = ru.Url (url)

    if not tags:
        tags  = dict()
        elems = filter (None, os.environ.get('RADICAL_SYNAPSE_TAGS', '').split(','))
        for elem in elems:
            if ':' in elem:
                key, val  = elem.split(':', 1)
                tags[key] = val
            else:
                tags[elem] = None


    command_idx = index_command (profile['cmd'], tags)
    print "index %s (%s) to %s" % (profile['cmd'], tags, command_idx)

    host = profile['sys'].get ('hostname')
    if not host:
        host = os.environ.get ('RADICAL_SYNAPSE_HOSTNAME', socket.gethostname())
        profile['sys']['hostname'] = host

    doc  = {'type'        : 'synapse_profile',
            'mode'        : mode,
            'command_idx' : command_idx,
            'command'     : profile['cmd'],
            'tags'        : tags,
            'profile'     : profile}



    if url.schema == 'mongodb':

        print 'store profile in db %s' % url

        [dbhost, port, dbname, _, _, _, _] = ru.split_dburl (url)

        db_client  = pymongo.MongoClient (host=dbhost, port=port)
        database   = db_client[dbname]
        collection = database['profiles']

        collection.insert (doc)


    elif url.schema == 'file':

        path = url.path

        if not os.path.isdir (path):
            os.system ('mkdir -p "%s"' % path)

        name = command_idx.split()[0]
      # for key, val in tags.iteritems():
      #     if val != None: name += "_%s:%s" % (key, val)
      #     else          : name += "_%s"    % (key)
        for tag in sorted(tags.keys()):
            if tags[tag] != None: name += "_%s" % tags[tag]
            else                : name += "_%s" % tag

        idx  = 0
        while True:
            fname = "%s/synapse_profile_%s_%s_%s_%03d.json" % (path, name, host, mode[0:3], idx)
            if not os.path.exists (fname):
                break
            idx += 1

        print 'store profile in file %s' % fname
        os.system ('mkdir -p "%s/"' % path)
        ru.write_json (doc, fname)



# ------------------------------------------------------------------------------
def get_profiles (command, tags=None, url=None, mode=None) :

    print command

    if not url:
        url = os.environ.get ('RADICAL_SYNAPSE_DBURL')

    if not url:
        print "warning: need dburl to retrieve profiles"
        return None

    url = ru.Url(url)

    if mode and not isinstance (mode, list):
        mode = [mode]

    if not tags:
        tags  = dict()
        elems = filter (None, os.environ.get('RADICAL_SYNAPSE_TAGS', '').split(','))
        for elem in elems:
            if ':' in elem:
                key, val  = elem.split(':', 1)
                tags[key] = val
            else:
                tags[elem] = None


    command_idx = index_command (command, tags)

    if url.schema == 'mongodb':

        [dbhost, port, dbname, _, _, _, _] = ru.split_dburl (url)

        db_client  = pymongo.MongoClient (host=dbhost, port=port)
        database   = db_client[dbname]
        collection = database['profiles']

        # FIXME: eval partial tags

        if mode:
            results = collection.find ({'type'        : 'synapse_profile',
                                        'tags'        : tags,
                                        'mode'        : {'$in': mode},  # FIXME: check
                                        'command_idx' : command_idx})
        else:
            results = collection.find ({'type'        : 'synapse_profile',
                                        'tags'        : tags,
                                        'command_idx' : command_idx})

        if  not results.count() :
            raise RuntimeError ("Could not get profile for %s at %s/profiles"
                    % (command, url))

        ret = list(results)


    elif url.schema == 'file':

        path = url.path

        if not os.path.isdir (path):
            raise ValueError ("dburl (%s) must point to an existing dir" % url)

        name = command_idx.split()[0]
      # for key, val in tags.iteritems():
      #     if val != None: name += "_%s:%s" % (key, val)
      #     else          : name += "_%s"    % (key)
        for tag in sorted(tags.keys()):
            if tags[tag] != None: name += "_%s" % tags[tag]
            else                : name += "_%s" % tag

      # print    "checking profiles %s/synapse_profile_%s_*.json" % (path, name)
        base   = "%s/synapse_profile_%s_*.json" % (path, name)
        fnames = glob.glob (base)
        ret    = list()
        for fname in fnames:

          # print 'reading profile %s' % fname

            doc     = ru.read_json_str (fname)
            use     = False
            docmode = doc['mode'][0:3]

            doc['fname'] = fname

            if doc['command'] == command:
                if not mode :
                    use = True
                elif docmode in mode:
                    use = True
                else:
                    print "skip: mode %s not in %s" % (docmode, mode)
            else:
                print "skip command %s" % command
                print "   ! command %s" % doc['command']

            if use:
                ret.append (doc)

        if not len(ret):
            raise LookupError ("No matching profile at %s" % base)

  # print 'retrieved %d profiles from %s' % (len(ret), url)
  # pprint.pprint (ret)

    return ret

# ------------------------------------------------------------------------------
#
def get_all_frames (command, tags=None, url=None, mode=None) :

    if not url:
        url = os.environ.get ('RADICAL_SYNAPSE_DBURL')

    if not url:
        print "warning: need dburl to retrieve profiles"
        return None

    docs = list()

    url = ru.Url (url)
    if url.scheme != 'file':
        raise ValueError ('can only handle file:// based dburls, not %s' % url)

    path = url.path

    for p in glob.glob ("%s/*/" % path):
        tmp_url = ru.Url (url)
        tmp_url.path = p
        tmp_docs = get_profiles (command, tags=tags, url=tmp_url, mode=mode)
        if tmp_docs:
            docs += tmp_docs

    return make_frames (docs)


# ------------------------------------------------------------------------------
#
def get_frames (command, tags=None, url=None, mode=None) :

    if not url:
        url = os.environ.get ('RADICAL_SYNAPSE_DBURL')

    if not url:
        print "warning: need dburl to retrieve profiles"
        return None

    docs = get_profiles (command, tags, url, mode)

    return make_frames (docs)


# ------------------------------------------------------------------------------
#
def make_frames (docs):

    frame_dicts = list()

    for doc in docs:

        profile = doc['profile']

        tags = doc['tags']
        mode = doc['mode'][0:3]

        cmd  = profile.get ('cmd',  "")
        sys  = profile.get ('sys',  {})
        sto  = profile.get ('sto',  {})
        cpu  = profile.get ('cpu',  {})
        mem  = profile.get ('mem',  {})
        sys  = profile.get ('sys',  {})
        time = profile.get ('time', {})

        frame_dict = {
            'host'         : sys['hostname'],
            'mode'         : mode,
            'tags'         : tags,
            'cmd'          : doc['command'],
            'cmd_idx'      : doc['command_idx'],

            'time_real'    : time['real'],
            'time_start'   : time['start'],

            'cpu_ops'      : cpu.get('ops'),
            'cpu_flops'    : cpu.get('flops'),
            'cpu_sequence' : cpu.get('sequence'),

            'mem_peak'     : mem.get('peak'),
            'mem_rss'      : mem.get('rss'),
            'mem_sequence' : mem.get('sequence'),
            'mem_size'     : mem.get('size'),

            'sto_read'     : sto.get('read'),
            'sto_write'    : sto.get('write'),
            'sto_sequence' : sto.get('sequence'),
        }

        for tag in tags:
            # FIXME: assumption is that tags are ints -- that is not save
            frame_dict['tag_%s'%tag] = float(tags[tag])

        frame_dicts.append(frame_dict)

    import pandas 
    frames = pandas.DataFrame (frame_dicts)

    return frames


# ------------------------------------------------------------------------------
#
def index_command (command, tags=None) :

    return str(command)


# ------------------------------------------------------------------------------

