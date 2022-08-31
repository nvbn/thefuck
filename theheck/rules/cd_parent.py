# Adds the missing space between the cd command and the target directory
# when trying to cd to the parent directory.
#
# Does not really save chars, but is fun :D
#
# Example:
# > cd..
# cd..: command not found


def match(command):
    return command.script == 'cd..'


def get_new_command(command):
    return 'cd ..'
