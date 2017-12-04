#!/usr/bin/env python

import os
import sys
import json
import pprint 
import radical.synapse as rs


sample_struct = ['cpu', 0, {'time'          : task_length,
                            'flops'         : 0,
                            'efficiency'    : 1 }]

def emu_source(src):

    info, ret, out = rs.emulate(src=src)
    pprint.pprint(info)


