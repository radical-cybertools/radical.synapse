
import synapse.utils

# ------------------------------------------------------------------------------

NOTHING       = 'synapse_nothing'
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
        return command


    if  mode  == PROFILE :
        ret = "python -c 'import synapse, sys; "\
              "info, ret, out = synapse.profile_command (\"\"\"%s\"\"\"); "\
              "print out; sys.exit (ret)'" % command
        return ret


    if  mode  == EMULATE :
        ret = "python -c 'import synapse, sys; "\
              "info, ret, out = synapse.emulate_command (\"\"\"%s\"\"\"); "\
              "print out; sys.exit (ret)'" % command
        return ret


