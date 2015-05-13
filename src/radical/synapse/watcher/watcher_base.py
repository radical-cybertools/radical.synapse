
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2015, RADICAL@Rutgers"
__license__   = "MIT"


import os
import time
import threading

from ..utils import timestamp

# number of samples per second
_SAMPLE_RATE = 1

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
    def _pre_process  (self)       : pass
    def _post_process (self)       : pass
    def _sample       (self, now)  : pass
    def _finalize     (self, info) : pass


    # --------------------------------------------------------------------------
    #
    def finalize (self, info) :

        try:
            self._finalize (info)

        except Exception as e:
            
            import traceback
            traceback.print_exc()

            print "Exception in finalize: %s" % e


    # --------------------------------------------------------------------------
    #
    def stop (self) :

        self._terminate.set()


    # --------------------------------------------------------------------------
    #
    def run (self) :

        try:

            self._config['sample_rate'] = float(os.environ.get('RADICAL_SYNAPSE_SAMPLERATE', _SAMPLE_RATE))

            # sample rate is samples per minute
            sleeptime = 1/self._config['sample_rate']

            self._pre_process(self._config)

            while not self._terminate.is_set():

                now = timestamp()
                self._sample(now)
                
                time.sleep (sleeptime)

            self._post_process()

          # print " ----- %s -----" % self.__class__
          # pprint.pprint (self._data)

        except Exception as e:

            import traceback
            traceback.print_exc()

            print "Exception in watcher: %s" % e


    # --------------------------------------------------------------------------
    #
    def get_data (self) :

        return self._data



# ------------------------------------------------------------------------------

