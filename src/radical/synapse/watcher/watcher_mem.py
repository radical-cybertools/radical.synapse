
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2015, RADICAL@Rutgers"
__license__   = "MIT"


import watcher_base as wb

from ..utils import human_to_number

# ------------------------------------------------------------------------------
#
# see http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
#
class WatcherMem (wb.WatcherBase) :

    # --------------------------------------------------------------------------
    #
    def __init__ (self, pid):

        self._old_sample = dict()
        self._tot_sample = dict()

        wb.WatcherBase.__init__(self, pid)


    def _pre_process  (self, config): 

        self._f = open('/proc/%s/status' % self._pid, 'r')
        self._data['mem']             = dict()
        self._data['mem']['sequence'] = list()

        self._f.seek(0,0)
        data = None
        try:
            data = self._f.read()
        except:
            pass

    
    # --------------------------------------------------------------------------
    #
    def _post_process (self): 

        self._f.close()

        # use the values from tot_sample as global total
        for key,val in self._tot_sample.iteritems():
            self._data['mem'][key] = val


    # --------------------------------------------------------------------------
    #
    def _sample (self, now) :

        try:
            self._f.seek(0,0)
            data = self._f.read()

        except Exception as e:
            # FIXME: use log
          # print "mem data source is gone (%s)" % e
            return

        sample = dict()
        memk   = {'VmSize' : 'size', 
                  'VmRSS'  : 'rss'}
        glob   = {'VmPeak' : 'peak'}

        for line in data.split('\n'):
            if not ':' in line:
                continue
            key, val = line.split (':', 1)
            if   key.strip() in memk : sample[memk[key]]            = human_to_number (val)
            elif key.strip() in glob : self._data['mem'][glob[key]] = human_to_number (val)


        # keep the max vals in tot_sample
        for key,val in sample.iteritems():
            self._tot_sample[key] = max(self._tot_sample.get(key, 0), val)


        # we don't want abs values but incremental changes
        for key in sample:

            val = sample[key]
            old = self._old_sample.get(key)

            if old:
                sample[key] = val - old

            self._old_sample[key] = val


        self._data['mem']['sequence'].append ([now, sample])


# ------------------------------------------------------------------------------

