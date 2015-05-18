
__author__    = "Radical.Utils Development Team (Andre Merzky)"
__copyright__ = "Copyright 2015, RADICAL@Rutgers"
__license__   = "MIT"


import os
import socket

import watcher_base as wb

from ..utils import human_to_number, PREFIX_ISO


# ------------------------------------------------------------------------------
#
class WatcherSys (wb.WatcherBase) :

    # --------------------------------------------------------------------------
    #
    def __init__ (self, pid):

        wb.WatcherBase.__init__(self, pid)


    # --------------------------------------------------------------------------
    #
    def _pre_process (self, config): 

        self._data['sys'] = dict()
        self._data['cpu'] = dict()


    # --------------------------------------------------------------------------
    #
    def _post_process (self): 

        with open ("/proc/cpuinfo") as proc_cpuinfo:

            cpu_freq         = 1 # in Hz
            num_sockets      = 1
            cores_per_socket = 1 
            core_siblings    = 1
            threads_per_core = 1
            flops_per_cycle  = 4 # see wikipedia on FLOPS
            flops_per_core   = flops_per_cycle * cpu_freq

            for line in proc_cpuinfo.readlines ()  :

                if  line.startswith ('model name') :
                    elems = line.split ('@')
                    if  elems[-1].endswith ('Hz\n') :
                        cpu_freq = max(cpu_freq, human_to_number (elems[-1], prefix=PREFIX_ISO))

                if  line.startswith ('cpu MHz') :
                    elems = line.split (':')
                    cpu_freq = max(cpu_freq, float(elems[-1]) * 1000*1000)

                if  line.startswith ('physical id') :
                    elems = line.split (':')
                    num_sockets = max(num_sockets, int(elems[-1])+1)

                if  line.startswith ('cpu cores') :
                    elems = line.split (':')
                    cores_per_socket = max(cores_per_socket, int(elems[-1]))

                if  line.startswith ('siblings') :
                    elems = line.split (':')
                    core_siblings = max(core_siblings, int(elems[-1]))

            threads_per_core = int(core_siblings / cores_per_socket)
            flops_per_core   = int(cpu_freq * flops_per_cycle)

        self._data['cpu']['num_sockets'      ] = num_sockets      
        self._data['cpu']['cores_per_socket' ] = cores_per_socket 
        self._data['cpu']['threads_per_core' ] = threads_per_core 
        self._data['cpu']['frequency'        ] = cpu_freq         
        self._data['cpu']['flops_per_cycle'  ] = flops_per_cycle  
        self._data['cpu']['flops_per_core'   ] = flops_per_core   

        self._data['sys']['hostname'] = os.environ.get('RADICAL_SYNAPSE_HOSTNAME', 
                                                       socket.gethostname())
        



# ------------------------------------------------------------------------------

