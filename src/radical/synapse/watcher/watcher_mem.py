
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

        wb.WatcherBase.__init__(self, pid)

    def _pre_process  (self, config): 

        self._f = open('/proc/%s/status' % self._pid, 'r')
        self._data['mem']             = dict()
        self._data['mem']['sequence'] = list()
        self._data['cpu']             = dict()
        self._data['cpu']['sequence'] = list()

        try:
            self._f.seek(0,0)
            data = self._f.read()
        except Exception as e:
            self.stop() 
            return

    
    # --------------------------------------------------------------------------
    #
    def _post_process (self): 

        self._f.close()


    # --------------------------------------------------------------------------
    #
    def _sample (self, now) :

        try:
            self._f.seek(0,0)
            data = self._f.read()
        except Exception as e:
            self.stop() 
            return

        item = dict()
        memk = {'VmSize' : 'size', 
                'VmRSS'  : 'rss'}
        glob = {'VmPeak' : 'peak'}
        for line in data.split('\n'):
            if not ':' in line:
                continue
            key, val = line.split (':', 1)
            if   key.strip() in memk        : item[memk[key]]              = human_to_number (val)
            elif key.strip() in glob        : self._data['mem'][glob[key]] = human_to_number (val)
            elif key.strip() in ['Threads'] :
                self._data['cpu']['sequence'].append([now,{'threads': int(val)}])

        self._data['mem']['sequence'].append ([now, item])


# ------------------------------------------------------------------------------

