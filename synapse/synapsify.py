
import synapse.utils

# ------------------------------------------------------------------------------

NOTHING       = None
PROFILE       = 'synapse_profile'
EMULATE       = 'synapse_emulate'

# ------------------------------------------------------------------------------
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
        synapse._logger.debug ("synapsify in : %s" % command)
        synapse._logger.debug ("synapsify out: %s" % command)
        return command


    if  mode  == PROFILE :
        synapse._logger.debug ("synapsify in :                     %s" % command)
      # ret = "python -c 'import synapse, sys; "\
      #       "info, ret, out = synapse.profile_command (\"\"\"%s\"\"\"); "\
      #       "print out; sys.exit (ret)'" % command
        ret = "synapse_profile.py '%s'" % command
        synapse._logger.debug ("synapsify out: %s" % ret)
        return ret


    if  mode  == EMULATE :
        synapse._logger.debug ("synapsify in :                     %s" % command)
      # ret = "python -c 'import synapse, sys; "\
      #       "info, ret, out = synapse.emulate_command (\"\"\"%s\"\"\"); "\
      #       "print out; sys.exit (ret)'" % command
        ret = "synapse_emulate.py '%s'" % command
        synapse._logger.debug ("synapsify out: %s" % ret)
        return ret


