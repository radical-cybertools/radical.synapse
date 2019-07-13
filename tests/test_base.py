#!/usr/bin/env python

import os

import radical.synapse       as rs


# ------------------------------------------------------------------------------
#
def test_base():

    os.environ['RADICAL_SYNAPSE_DBURL'] = "file://%s" % os.getcwd ()
    os.environ['RADICAL_SYNAPSE_TAGS']  = "cpu"
    info, _, _ = rs.emulate ('test cpu')

    os.environ['RADICAL_SYNAPSE_TAGS']  = "mem"
    info, _, _ = rs.emulate ('test mem')

    os.environ['RADICAL_SYNAPSE_TAGS']  = "sto"
    info, _, _ = rs.emulate ('test sto')

    os.environ['RADICAL_SYNAPSE_TAGS']  = ""
    info, _, _ = rs.emulate ('test')
    info, _, _ = rs.execute ('sleep 3')
    info, _, _ = rs.profile ('sleep 3')
    info, _, _ = rs.emulate ('sleep 3')


# ------------------------------------------------------------------------------

