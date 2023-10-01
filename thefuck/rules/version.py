# Fixes incorrect usage of version commands
#
# Example :
# > git -v
# Here the correct usage is
# > git --version


def match(command):
    return ('-v' in command.script)


def get_new_command(command):
    if '--version' in command.script:
        return command.script_parts[0] + ' -v'
    else:
        return command.script_parts[0] + ' --version'
