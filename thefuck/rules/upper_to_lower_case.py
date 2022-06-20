from thefuck.utils import get_all_executables, which

# this rule is activated when the typed command is
# in uppercase letters and if the command is not 
# executed. However in order to activate this rule
# it is necessary the first word of the whole command
# to be valid.
def match(command):
    return (command.script.isupper()
    	    and not which(command.script_parts[0])
            and ('not found' in command.output
                 or 'is not recognized as' in command.output)
            and (command.script_parts[0].lower() in get_all_executables()))

# returns the same command in lowercase letters
def get_new_command(cmd):
    return cmd.script.lower()


requires_output = False
priority = 100