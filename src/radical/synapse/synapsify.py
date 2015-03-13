
import radical.synapse

# ------------------------------------------------------------------------------
#

NOTHING = None
PROFILE = 'synapse_profile'
EMULATE = 'synapse_emulate'

# ------------------------------------------------------------------------------
#
def synapsify (command, mode=NOTHING) :
    """
    Uses synapse to transform the given command in three possible ways,
    depending on mode::

        NOTHING: 
            empty transormation -- duh!  This only exists to avoid case
            switches in the application code

        PROFILE:
            the command is run under a profile, which will, duh, profile the
            application run, and store the results in the synapse MongoDB
            database.

        EMULATE:
            the command is replaces with a synapse emulation -- the emulation
            parameters are pulled from the synapse MongoDB database.  If those
            parameters cannot be found, an exception is raised.
    """

    if  mode == NOTHING :
        radical.synapse._logger.debug ("synapsify in : %s" % command)
        radical.synapse._logger.debug ("synapsify out: %s" % command)
        return command


    if  mode  == PROFILE :
        ret = "radical-synapse-profile.py '%s'" % command
        radical.synapse._logger.debug ("synapsify in : %s" % command)
        radical.synapse._logger.debug ("synapsify out: %s" % ret)
        return ret


    if  mode  == EMULATE :
        ret = "radical-synapse-emulate.py '%s'" % command
        radical.synapse._logger.debug ("synapsify in : %s" % command)
        radical.synapse._logger.debug ("synapsify out: %s" % ret)
        return ret


# ------------------------------------------------------------------------------

