
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2015, RADICAL@Rutgers"
__license__   = "MIT"


import watcher_base as wb

from ..utils import human_to_number


# ------------------------------------------------------------------------------
#
class WatcherIO (wb.WatcherBase) :

    # --------------------------------------------------------------------------
    #
    def __init__ (self, pid):

        wb.WatcherBase.__init__(self, pid)

    
    # --------------------------------------------------------------------------
    #
    def _pre_process  (self): 

        self._f = open('/proc/%s/io' % self._pid, 'r')
        self._data['i_o']             = dict()
        self._data['i_o']['sequence'] = list()

    
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
        keys = {'rchar' : 'read',
                'wchar' : 'write'}
        for line in data.split('\n'):
            if not ':' in line:
                continue
            key, val = line.split (':', 1)
            if  key.strip() in keys : 
                item[keys[key]] = human_to_number (val)


        self._data['i_o']['sequence'].append ([now, item])


# ------------------------------------------------------------------------------

