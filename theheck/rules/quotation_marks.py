# Fixes careless " and ' usage
#
# Example:
# > git commit -m 'My Message"


def match(command):
    return '\'' in command.script and '\"' in command.script


def get_new_command(command):
    return command.script.replace('\'', '\"')
