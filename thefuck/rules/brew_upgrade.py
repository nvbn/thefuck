# Appends --all to the brew upgrade command
#
# Example:
# > brew upgrade
# Warning: brew upgrade with no arguments will change behaviour soon!
# It currently upgrades all formula but this will soon change to require '--all'.


def match(command):
    return command.script == 'brew upgrade'


def get_new_command(command):
    return command.script + ' --all'
