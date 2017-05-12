#!/bin/sh

VE=./ve
VE=/lustre/atlas2/csc230/scratch/merzky1/radical.pilot.sandbox/ve_synapse

. $VE/bin/activate


export OMP_NUM_THREADS=$1
export RADICAL_SYNAPSE_USE_OPENMP=1

start=$(date +%s)
radical-synapse-sample -s 10 -f 10000000000
stop=$(date +%s)

echo "diff: $((stop-start))"
 
