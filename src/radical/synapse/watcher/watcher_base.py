
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2015, RADICAL@Rutgers"
__license__   = "MIT"


import time
import threading

from ..utils import timestamp

_SAMPLE_RATE = 0.1
_SAMPLE_RATE = 0.5

# ------------------------------------------------------------------------------
#
class WatcherBase (threading.Thread) :

    # --------------------------------------------------------------------------
    #
    def __init__ (self, pid):

        threading.Thread.__init__(self)
        self._terminate = threading.Event()
        self._pid       = pid
        self._data      = dict()
        self._config    = dict()

        self.start ()


    # --------------------------------------------------------------------------
    #
    # This is the API which watcher implementations overload.
    #
    def _pre_process  (self)      : pass
    def _post_process (self)      : pass
    def _sample       (self, now) : pass


    # --------------------------------------------------------------------------
    #
    def stop (self) :

        self._terminate.set()


    # --------------------------------------------------------------------------
    #
    def run (self) :

        try:

            self._config['sample_rate'] = _SAMPLE_RATE

            self._pre_process(self._config)

            while not self._terminate.is_set():

                now = timestamp()
                self._sample(now)
                time.sleep (_SAMPLE_RATE)

            self._post_process()

          # print " ----- %s -----" % self.__class__
          # pprint.pprint (self._data)

        except Exception as e:
            print "Exception in watcher: %s" % e
          # raise


    # --------------------------------------------------------------------------
    #
    def get_data (self) :

        return self._data



# ------------------------------------------------------------------------------

