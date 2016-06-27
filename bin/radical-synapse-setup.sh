#!/bin/sh


if test -d $HOME/ve.synapse
then
    exit
fi

module load python || true
virtualenv  $HOME/ve.synapse 

.  $HOME/ve.synapse/bin/activate

# pip install aimes.skeleton
# pip install radical.synapse

pip install git+https://github.com/radical-cybertools/radical.synapse@feature/named_storage
pip install git+https://github.com/applicationskeleton/Skeleton@feature/synapse_tasks

radical-synapse-sample -t 3

