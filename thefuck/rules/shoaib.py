# Adds the missing space between the ls command and the option (i.e. -l)
# when trying to ls with options.
#
# Does not really save chars, but it is a fun and my first contribution ever in open source project.
#
# Example:
# > ls-l
# ls-l: command not found


def match(command):
    return command.script == 'ls-l'


def get_new_command(command):
    return 'ls -l'
