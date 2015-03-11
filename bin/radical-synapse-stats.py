#!/usr/bin/env python

import os
import sys
import pprint
import pymongo
import radical.utils       as ru
import radical.pilot       as rp
import radical.pilot.utils as rpu


_DEFAULT_DBURL = 'mongodb://user:password@localhost:27017/radicalpilot/'
_DEFAULT_DBURL = 'mongodb://user:password@ec2-184-72-89-141.compute-1.amazonaws.com:27017/radicalpilot/'
_DEFAULT_DBURL = 'mongodb://localhost:27017/synapse_montage_01'

if  'RADICAL_SYNAPSE_DBURL' in os.environ :
    _DEFAULT_DBURL = os.environ['RADICAL_SYNAPSE_DBURL']


_DEFAULT_DBURL = str(ru.Url(_DEFAULT_DBURL))


# ------------------------------------------------------------------------------
#
def my_round (x, base=5) :

    # thanks to 
    # http://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python

    return int(base * round(float(x) / base))


# ------------------------------------------------------------------------------
#
def usage (msg=None, noexit=False) :

    if  msg :
        print "\n      Error: %s" % msg

    print """
      usage     : %s -m <mode> [-u dburl] [-d dbname]
      example   : %s -m stat    -u mongodb://user:password@localhost/ -d synapse_test


      modes     :

        help    : show this message
        list    : show  a  list   of databases
        tree    : show  a  tree   of record entries
        dump    : show  a  tree   of record entries, with details
        stat    : show statistics of record entries
        plot    : plot record entries

      arguments :
        
        -u      : database URL
        -d      : database name
        -c      : cachedir where <sid>.json caches are kept (also needs -s)
        -t      : terminal type for plotting (pdf and/or png, default is both)


      The default command is 'list'.  
      The default MongoDB is '%s'.
      
""" % (sys.argv[0], sys.argv[0], _DEFAULT_DBURL)

    if  msg :
        sys.exit (1)

    if  not noexit :
        sys.exit (0)


# ------------------------------------------------------------------------------
#
def dump_database (mongo, db, dbname, cachedir) :

    print "dbname : %s" % dbname
    handle_database (mongo, db, 'dump', dbname, cachedir, None)


# ------------------------------------------------------------------------------
#
def tree_database (mongo, db, dbname, cachedir) :

    handle_database (mongo, db, 'tree', dbname, cachedir, None)


# ------------------------------------------------------------------------------
#
def list_databases (mongo, db, dbname, cachedir) :

    if  dbname :
        print "invalid dbname parameter on 'list'"
        sys.exit (-1)

    dbnames = mongo.database_names ()

    if  not dbnames :
        print 'no databases at %s' % mongo

    else :
        print "Databases:"
        for dbname in dbnames :
            if dbname not in ['local'] :
                print "  %s" % dbname


# ------------------------------------------------------------------------------
def sort_database (mongo, db, dbname, cachedir) :

    docs = rpu.get_database_docs (mongo, db, dbname, cachedir=cachedir)

    print "pilot managers :" 
    for doc in docs['pmgr'] :
        print "  %s" %  doc['_id']

    print "pilots :" 
    for doc in docs['pilot'] :
        print "  %s" %  doc['_id']

    print "unit manager"
    for doc in docs['umgr'] :
        print "  %s" %  doc['_id']

    print "units"
    for doc in docs['unit'] :
        print "  %s" %  doc['_id']


# ------------------------------------------------------------------------------
def hist_database (mongo, db, dbname, cachedir) :

    events    = rpu.get_database_events   (mongo, db, dbname, cachedir=cachedir)

    if  not events :
        print "no records found in database %s" % dbname
        sys.exit (-1)

    start = events[0][4]

    # ascii output of time sorted events and slot history

    print "database: %s" % dbname
    print "start   : %s" % str(ru.time_stamp (start))

    for e in events :
        seconds = ru.time_diff (start, e[4])
        print "          %08.2fs : %10s : %15s : %20s (%s)" % (seconds, e[1], e[2], e[5], e[0])


    if  slothists :
        for pilot_info in slothists :
            print "pilot   : %s" % pilot_info['pilot_id']
            for slothist in pilot_info['slothist'] :
                seconds = ru.time_diff (start, slothist['timestamp'])
                print "          %08.2fs : %s" % (seconds, str(slothist['slotstate']))


# ------------------------------------------------------------------------------
def get_stats (docs, events, slothist) :

    n_units               = 0
    n_pilots              = 0
    unit_state_durations  = dict()
    pilot_stats           = dict()
    units                 = dict()

    pilot_stats['pilots'] = dict()

    for cu in docs['unit'] :
        units[str(cu['_id'])] = cu

    for doc in docs['pilot'] :

        n_pilots   += 1
        pid         = str(doc['_id'])
        pilot_info  = dict()

        pilot_info['resource']     = doc['description']['resource']
        pilot_info['cores']        = doc['description']['cores']
        pilot_info['n_units']      = 0
        pilot_info['unit_states']  = dict()
        pilot_info['pilot_states'] = list()

        # we assume that states are time-ordered
        state = doc['statehistory'][0]['state']
        start = doc['statehistory'][0]['timestamp']
        for t in doc['statehistory'][1:] :
            ts = t['timestamp']
            s  = t['state']
            pilot_info['pilot_states'].append ({'state'    : state, 
                                                'duration' : ru.time_diff(start, ts)})
            state = s
            start = ts

        for cu in doc['unit_ids'] :
            uid                    = str(cu)
            n_units               += 1
            pilot_info['n_units'] += 1

            if  not uid in units :
                print 'unknonwn unit %s' % uid
                sys.exit ()

            unit_doc = units[uid]
            state    = unit_doc['statehistory'][0]['state']
            start    = unit_doc['statehistory'][0]['timestamp']

            for t in unit_doc['statehistory'][1:] :
                ts = t['timestamp']
                s  = t['state']

                if not state in pilot_info['unit_states'] :
                    pilot_info['unit_states'][state]        = dict()
                    pilot_info['unit_states'][state]['dur'] = list()

                pilot_info['unit_states'][state]['dur'].append (ru.time_diff(start, ts))
                state = s
                start = ts

        pilot_runtime = (doc['finished'] - doc['started']) * len (slothist[pid]['slots'])
        pilot_busy = 0.0
        for slot in slothist[pid]['slot_infos'] :
            for slot_used in slothist[pid]['slot_infos'][slot] :
                pilot_busy += slot_used[1] - slot_used[0]

        pilot_info['started']     = doc['started']
        pilot_info['finished']    = doc['finished']
        pilot_info['cpu_burned']  = pilot_runtime
        pilot_info['cpu_used']    = pilot_busy
        pilot_info['utilization'] = pilot_busy * 100 / pilot_runtime

        for s in pilot_info['unit_states'] :
            import numpy
            array = numpy.array (pilot_info['unit_states'][s]['dur'])
            pilot_info['unit_states'][s]['num' ] = len        (array)
            pilot_info['unit_states'][s]['mean'] = numpy.mean (array)
            pilot_info['unit_states'][s]['std' ] = numpy.std  (array)
            pilot_info['unit_states'][s]['dur' ] = list()


        pilot_stats['pilots'][pid] = pilot_info

    pilot_stats['n_pilots'] = n_pilots

    return pilot_stats

    
# ------------------------------------------------------------------------------
def stat_database (mongo, db, dbname, cachedir) :

    print

    records = db.collection_names()

    for record in records :
        docs = db[record].find()

    for doc in docs :
        print "index: %s" % doc['command_idx']

        for profile in doc['profiles'] :
            print "  command: %s" % profile['cmd']
            print "  time   : %s" % profile['time']['real']
            print "  cpu    : %s" % len(profile['cpu']['sequence'])
            print "  io     : %s" % len(profile['i_o']['sequence'])

            mem = profile['mem']
            print "  mem: %s" % mem['peak']
            print "# %15s  %15s  %15s" % ('time', 'size', 'rss')
            for s in mem['sequence']:
                print '  %15s  %15s  %15s' % (s[0], s[1]['size'], s[1]['rss'])


# ------------------------------------------------------------------------------
def plot_database (mongo, db, dbname, cachedir, term) :
    """
    plot results :P
    """

    print

    records = db.collection_names()

    for record in records :
        docs = db[record].find()

    for doc in docs :
        print "index: %s" % doc['command_idx']

        for profile in doc['profiles'] :

            perf = profile['time']
            mem  = profile['mem']
            cpu  = profile['cpu']
            io   = profile['i_o']

            print "  command: %s" % profile['cmd']
            print "  time   : %s" % profile['time']['real']
            print "  cpu    : %s" % len(profile['cpu']['sequence'])
            print "  io     : %s" % len(profile['i_o']['sequence'])
            print "  mem    : %s" % mem['peak']

            dat = open("/tmp/rs.%s.mem.dat" % dbname, "w")
            dat.write("# %15s  %15s  %15s\n" % ('time', 'size', 'rss'))
            for s in mem['sequence']:
                dat.write('  %15s  %15s  %15s\n' 
                         % (s[0], s[1]['size'], s[1]['rss']))
            dat.close()

            dat = open("/tmp/rs.%s.io.dat" % dbname, "w")
            dat.write("# %15s  %15s  %15s\n" % ('time', 'read', 'write'))
            for s in io['sequence']:
                dat.write('  %15s  %15s  %15s\n' 
                         % (s[0], s[1]['read'], s[1]['write']))
            dat.close()

    sys.exit()




    docs      = rpu.get_database_docs     (mongo, db, dbname, cachedir=cachedir)
    events    = rpu.get_database_events   (mongo, db, dbname, cachedir=cachedir)

    if  not events :
        print "no records found in database %s" % dbname
        sys.exit (-1)

    start      = events[0][4]
    pids       = list()
    maxtime    = 0.0
    maxslots   = 0
    nodesize   = 0
    slots      = list()
    hosts      = list()
    delete_me  = list()
    maxqueue   = 0

    # some data cleanup
    for doc in docs['pilot'] :
        if  not doc['nodes'] :
            doc['nodes'] = list()
        if  not doc['cores_per_node'] :
            doc['cores_per_node'] = 1

    # the plots look nicer if the largest pilots are plotted first, and smaller
    # ones are overlayed.  Thus we sort the pilot docs by by size (reversed).
    # Pilot's of same sizes are ordered as-is.
    pilot_sizes = list()
    for doc in docs['pilot'] :
        cores = len(doc['nodes']) * int(doc['cores_per_node'])
        pilot_sizes.append (cores)


    pilot_docs = list()
    for pilot_size in sorted (pilot_sizes, reverse=True) :
        for doc in docs['pilot'] :
            cores = len(doc['nodes']) * int(doc['cores_per_node'])
            if  cores == pilot_size :
                if  doc not in pilot_docs :
                    pilot_docs.append (doc)

    for pilot in pilot_docs :

        pid = str(pilot['_id'])
        pids.append (pid)
        hosts.append (ru.Url (pilot['sandbox']).host.split('.')[0])

        with open ("/tmp/rp.%s.pilot.states.%s.dat" % (dbname, pid), "w") as dat :
            for event in pilot['statehistory'] :
                etag    = _EVENT_ENCODING['pilot'].get (event['state'], 0)
                seconds = ru.time_diff (start, event['timestamp'])
                maxtime = max (maxtime, seconds)
                dat.write (" %10.2f  %-25s\n" % (seconds, etag))
            dat.write ("\n")
            delete_me.append (dat.name)
            
        with open ("/tmp/rp.%s.pilot.callbacks.%s.dat" % (dbname, pid), "w") as dat :
            if  'callbackhistory' in pilot :
                for event in pilot['callbackhistory'] :
                    etag    = _EVENT_ENCODING['pilot'].get (event['state'], 0)
                    seconds = ru.time_diff (start, event['timestamp'])
                    maxtime = max (maxtime, seconds)
                    dat.write ("%10.2f  %-25s\n" % (seconds, etag))
                dat.write ("\n")
            else :
                print 'no pilot callbacks'
            delete_me.append (dat.name)

            
        with open ("/tmp/rp.%s.unit.states.%s.dat" % (dbname, pid), "w") as dat :

            for unit_id in pilot['unit_ids'] :

                for unit in docs['unit'] :
                    if  unit_id == str(unit['_id']) :
                        for event in unit['statehistory'] :
                            etag    = _EVENT_ENCODING['unit'].get (event['state'], 0)
                            seconds = ru.time_diff (start, event['timestamp'])
                            maxtime = max (maxtime, seconds)
                            dat.write (" %10.2f  %-25s\n" % (seconds, etag))
                        dat.write ("\n")
            delete_me.append (dat.name)
            
        with open ("/tmp/rp.%s.unit.callbacks.%s.dat" % (dbname, pid), "w") as dat :
            for unit_id in pilot['unit_ids'] :
                for unit in docs['unit'] :
                    if  unit_id == str(unit['_id']) :
                        if  'callbackhistory' in unit :
                            for event in unit['callbackhistory'] :
                                etag    = _EVENT_ENCODING['unit'].get (event['state'], 0)
                                seconds = ru.time_diff (start, event['timestamp'])
                                maxtime = max (maxtime, seconds)
                                dat.write (" %10.2f  %-25s\n" % (seconds, etag))
                            dat.write ("\n")
            delete_me.append (dat.name)

            
        with open ("/tmp/rp.%s.pilot.queue.%s.dat" % (dbname, pid), "w") as dat :

            queue_size = 0
            queued     = list()
            dequeued   = list()

            dat.write ("%10.2f  %6d\n" % (0, queue_size))


            for event in events :
                if  event[0] == 'state' and \
                    event[1] == 'unit'  and \
                    event[3] ==  pid    :
                    uid = event[2]

                    if  _EVENT_ENCODING['unit'][event[5]] > _EVENT_ENCODING['unit'][rp.NEW] :
                        if  not uid in queued :
                            queued.append (uid)
                            seconds     = ru.time_diff (start, event[4])
                            queue_size += 1
                            maxqueue    = max (maxqueue, queue_size)
                            dat.write ("%10.2f  %6d\n" % (seconds, queue_size))

                    if  _EVENT_ENCODING['unit'][event[5]] > _EVENT_ENCODING['unit'][rp.EXECUTING] :
                        if  not uid in dequeued :
                            dequeued.append (uid)
                            seconds     = ru.time_diff (start, event[4])
                            queue_size -= 1
                            dat.write ("%10.2f  %6d\n" % (seconds, queue_size))


        with open ("/tmp/rp.%s.pilot.slots.%s.dat" % (dbname, pid), "w") as dat :

            slothist = slothists[pid]
            slotnum  = len(slothist['slots'])
            maxslots = max(slotnum,maxslots)

            slots.append (slotnum)

            slot_idx = 0
            for slot in slothist['slots'] :

                slot_idx += 1
                used = False

                for entry in slothist['slot_infos'][slot] :

                    busy_start = ru.time_diff (start, entry[0])
                    busy_stop  = ru.time_diff (start, entry[1])

                    dat.write ("%10.2f  %6d\n" % (busy_start, slot_idx))
                    dat.write ("%10.2f  %6d\n" % (busy_stop,  slot_idx))
                    dat.write ("\n")

                dat.write ("\n")

            delete_me.append (dat.name)

    pilotnum = len(pids)

    timetics = 10
    for i in range(1,10) :
        if  maxtime  > 1*(10**i) :
            timetics = 1*(10**(i-1))
        if  maxtime  > 2*(10**i) :
            timetics = 2*(10**(i-1))
        if  maxtime  > 5*(10**i) :
            timetics = 5*(10**(i-1))

  # mtimetics = 10

    plotfile = "%s/radicalpilot-stats.plot" % os.path.dirname (__file__)
    plotname = os.environ.get ('RP_PLOTNAME', None)

    # if maxslots and maxqueue differ by max 25% then we use the same scale.  If
    # maxslots is larger we also use the same scale.
    max_scale  = max(maxslots, maxqueue)
    min_scale  = min(maxslots, maxqueue)
    mean_scale = (maxslots+maxqueue)/2
    scale_25   = 0.25 * mean_scale

    if  maxslots > maxqueue :
        slotsscale = maxslots+(nodesize/2)
        queuescale = maxslots+(nodesize/2)

    elif (mean_scale + scale_25) > max_scale and \
        (mean_scale - scale_25) < min_scale :
        slotsscale = maxslots+(nodesize/2)
        queuescale = maxslots+(nodesize/2)

    else :
        slotsscale = maxslots+(nodesize/2)
        queuescale = maxqueue+(nodesize/2)

    slotsscale = int(max(slotsscale, maxslots*1.1))
    queuescale = int(max(queuescale, maxqueue*1.1))

    terms = " ".join (term.split (','))

                                         
    cmd  = "gnuplot -e  maxtime=%d "        % int(maxtime+10)
    cmd +=        " -e  timetics=%d "       % timetics
  # cmd +=        " -e  mtimetics=%d "      % mtimetics
    cmd +=        " -e  maxslots=%d "       % maxslots
    cmd +=        " -e  maxqueue=%d "       % maxqueue
    cmd +=        " -e  slotsscale=%d "     % slotsscale
    cmd +=        " -e  queuescale=%d "     % queuescale
    cmd +=        " -e  'slotnum_list=\""
    for idx,pid in enumerate(pids) :
        cmd +=    "%d "     % (slots[idx])
    cmd +=        "\"'"
    cmd +=        " -e  nodesize=%d "       % nodesize
    cmd +=        " -e 'dbname=\"%s\"' "    % dbname
    cmd +=        " -e 'sname=\"%s\"' "     % session_name
    cmd +=        " -e 'terms=\"%s\"' "     % terms
    cmd +=        " -e 'plottitle=\"RADICAL-Pilot\\n============="
    if plotname :
        cmd +=    "\\n[%s]" % plotname
    cmd +=        "\\nPilot and Unit Event Traces\\nSession %s\"' " % session_name
    cmd +=        " -e  pilot_num=%d "       % len(pids)
    cmd +=        " -e  'pilot_name_list=\""
    for idx,pid in enumerate(pids) :
        cmd +=    "%s[%d] " % (hosts[idx], slots[idx])
    cmd +=        "\"'"
    cmd +=        " -e  'pilot_id_list=\""
    for idx,pid in enumerate(pids) :
        cmd +=    "%s "       % (pids[idx])
    cmd +=        "\"'"
    cmd +=        "     %s "                        % plotfile

  # print cmd
    print "\nplotting..."
    os.system (cmd) 

    if  plotname :
        os.system ("mv %s.png %s.png" % (dbname, plotname))
        os.system ("mv %s.pdf %s.pdf" % (dbname, plotname))

    for filename in delete_me :
      # print "removing %s" % filename
        try :
          # os.remove (filename)
            pass
        except Exception as e :
            print "Error removing %s: %s" % (filename, str(e))

    DO_SPLOTS = False
    if  not DO_SPLOTS :
        return


    # --------------------------------------------------------------------------
    #
    # also do splots
    #
    entity_states = dict ()

    BEGIN  = ">"
    END    = "<"
    ONCE   = "!"
    COLORS = {rp.NEW                     : ' 1',
              rp.UNSCHEDULED             : ' 2',
              rp.PENDING_INPUT_STAGING   : ' 3',
              rp.STAGING_INPUT           : ' 4',
              rp.PENDING_EXECUTION       : ' 5',
              rp.SCHEDULING              : ' 6',
              "Allocating"               : ' 8',
              rp.EXECUTING               : ' 8',
              rp.PENDING_OUTPUT_STAGING  : ' 9',
              rp.STAGING_OUTPUT          : '10',
              rp.DONE                    : '11',
              rp.CANCELED                : '12',
              rp.FAILED                  : '13'}

    for pilot in docs['pilot'] :

        this_pid = str(pilot['_id'])

        with open ("/tmp/rp.%s.pilot.slots.%s.sdat" % (dbname, pid), "w") as dat :

            for e in events :

                etype   = e[0]
                otype   = e[1]
                uid     = e[2]
                pid     = e[3]
                ts      = e[4]
                state   = e[5]
                doc     = e[6]

                if  pid != this_pid :
                    continue

                if  otype == 'unit' :

                    if 'slots' in doc :
                        slots = doc['slots']
                    else :
                        pprint.pprint (doc)
                        slots = '?'

                    color = COLORS[state]

                    for slot in slots :

                        if  not uid in entity_states :
                            
                            if  state not in [rp.EXECUTING] :
                                continue

                            entity_states[uid] = state
                          # print      "%s %s%s %s"   % (ts, BEGIN, slot, COLORS[state])
                            dat.write ("%s %s%s %s\n" % (ts, BEGIN, slot, COLORS[state]))

                        else :
                            old_state = entity_states[uid]
                          # print      "%s %s%s %s"   % (ts, END,   slot, COLORS[old_state])
                            dat.write ("%s %s%s %s\n" % (ts, END,   slot, COLORS[old_state]))

                            entity_states[uid] = state
                          # print      "%s %s%s %s"   % (ts, BEGIN, slot, COLORS[state])
                            dat.write ("%s %s%s %s\n" % (ts, BEGIN, slot, COLORS[state]))


    for pilot in docs['pilot'] :

        this_pid = str(pilot['_id'])

        with open ("/tmp/rp.%s.pilot.units.%s.sdat" % (dbname, pid), "w") as dat :

            entity_states = dict()
            idxs          = list()

            # index the units by the start of their EXECUTING state
            for e in events :

                etype = e[0]
                otype = e[1]
                uid   = e[2]
                pid   = e[3]
                ts    = e[4]
                state = e[5]
                doc   = e[6]

                if  pid != this_pid :
                    continue

                if  otype == 'unit' :
                    if  state in [rp.EXECUTING] :
                        idxs.append (uid)

            for idx_id in idxs :

                for e in events :

                    etype = e[0]
                    otype = e[1]
                    uid   = e[2]
                    pid   = e[3]
                    ts    = e[4]
                    state = e[5]
                    doc   = e[6]

                    if  idx_id != uid :
                        continue

                    if  pid != this_pid :
                        continue

                    if  otype == 'unit' :

                        if 'slots' in doc :
                            slots = doc['slots']
                        else :
                            slots = '?'

                        for slot in slots :

                            if  not uid in entity_states :

                                entity_states[uid] = state

                              # print      "%s %s%s %s"   % (ts, BEGIN, uid, COLORS[state])
                                dat.write ("%s %s%s %s\n" % (ts, BEGIN, uid, COLORS[state]))

                            else :

                                old_state = entity_states[uid]
                              # print      "%s %s%s %s"   % (ts, END,   uid, COLORS[old_state])
                                dat.write ("%s %s%s %s\n" % (ts, END,   uid, COLORS[old_state]))

                                entity_states[uid] = state
                              # print      "%s %s%s %s"   % (ts, BEGIN, uid, COLORS[state])
                                dat.write ("%s %s%s %s\n" % (ts, BEGIN, uid, COLORS[state]))


# ------------------------------------------------------------------------------
def handle_database (mongo, db, mode, dbname, cachedir, pname) :
    """
    For the given db, traverse collections
    """

    # FIXME: cache(dir) is not used

    print " +-- db   %s" % dbname

    cnames = db.collection_names()

    for name in cnames :

        if  mode == 'list' and not cname :
            print " | +-- coll %s" % name

        elif  mode == 'remove' and not pname :
            try :
                db.drop_collection (name)
                print "  removed collection %s" % name
            except :
                pass # ignore errors

        else :
            handle_coll (mongo, db, mode, name, pname)



# ------------------------------------------------------------------------------
def handle_coll (mongo, db, mode, cname, pname) :
    """
    For a given collection, traverse all documents
    """

    if 'indexes' in cname :
        return

    collection = db[cname]
    print " | +-- coll %s" % cname

    docs = collection.find ()

    for doc in docs :

        name = doc['_id']

        if  mode == 'list' and not pname :
            print " | | +-- doc  %s  [%3s] [%s] " \
                    % (name, len(doc['profiles'][0]['mem']['sequence']), 
                       doc['command_idx'])

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
        pprint.pprint (doc)
        print " | | +-- doc  %s  [%3s] [%s] " \
                % (name, len(doc['profiles'][0]['mem']['sequences']), 
                   doc['command_idx'])
        for key in doc :
            print " | | | +-- %s" % (key)

    elif  mode == 'dump' :
        print " | | +-- doc  %s" % (name)
        for key in doc :
            txt_in  = pprint.pformat (doc[key])
            txt_out = ""
            lnum    = 1
            for line in txt_in.split ('\n') :
                if  lnum != 1 :
                    txt_out += ' | | | |                '
                txt_out += line
                txt_out += '\n'
                lnum    += 1

            print " | | | +-- %-10s : %s" % (key, txt_out[:-1]) # remove last \n
# ------------------------------------------------------------------------------
# 
def parse_commandline():

    return options


# ------------------------------------------------------------------------------
#
if __name__ == '__main__' :

    import optparse
    parser = optparse.OptionParser (add_help_option=False)

    parser.add_option('-d', '--dbname',    dest='dbname')
    parser.add_option('-u', '--dburl',     dest='url')
    parser.add_option('-m', '--mode',      dest='mode')
    parser.add_option('-c', '--cachedir',  dest='cachedir')
    parser.add_option('-t', '--terminal',  dest='term')
    parser.add_option('-h', '--help',      dest='help', action="store_true")

    options, args = parser.parse_args ()

    if  args :
        usage ("Too many arguments (%s)" % args)

    if  options.help :
        usage ()

    if  options.mode in ['help'] : 
        usage ()

    if  not options.mode :
        usage ("No mode specified")

    if  not options.url : 
        options.url = _DEFAULT_DBURL


    mode     = options.mode 
    url      = options.url
    dbname   = options.dbname
    term     = options.term
    cachedir = options.cachedir


    if  not term :
        term = "pdf,png"

    if  not cachedir :
        cachedir = os.getcwd ()

    if  not os.path.isdir (cachedir) :
        usage ("%s is no valid cachedir" % cachedir)

    url = ru.Url (options.url)

    print "modes   : %s" % mode
    print "db url  : %s" % url
    print "cachedir: %s" % cachedir
    mongo, db, _, cname, pname = ru.mongodb_connect (str(url), url)

    print dbname


    for m in mode.split (',') :

        if  m not in ['list', 'dump', 'tree', 'hist', 'sort', 'stat', 'plot', 'help'] : 
            usage ("Unsupported mode '%s'" % m)

        if   m == 'list' : list_databases (mongo, db, dbname, cachedir)
        elif m == 'tree' : tree_database  (mongo, db, dbname, cachedir) 
        elif m == 'dump' : dump_database  (mongo, db, dbname, cachedir)
        elif m == 'sort' : sort_database  (mongo, db, dbname, cachedir)
        elif m == 'hist' : hist_database  (mongo, db, dbname, cachedir)
        elif m == 'stat' : stat_database  (mongo, db, dbname, cachedir)
        elif m == 'plot' : plot_database  (mongo, db, dbname, cachedir, term)
        elif m == 'help' : usage (noexit=True)
        else             : usage ("unknown mode '%s'" % mode)

    # ------------------------------------------------------------------------------------
    mongo.disconnect ()

# ------------------------------------------------------------------------------

