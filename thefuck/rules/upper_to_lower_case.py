from thefuck.utils import get_all_executables, which


def match(command):
    return (command.script.isupper()
    	    and not which(command.script_parts[0])
            and ('not found' in command.output
                 or 'is not recognized as' in command.output)
            and (command.script_parts[0].lower() in get_all_executables()))


def get_new_command(cmd):
    return cmd.script.lower()


requires_output = False
priority = 100