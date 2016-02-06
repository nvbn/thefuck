# Appends --all to the brew upgrade command
#
# Example:
# > brew upgrade
# Warning: brew upgrade with no arguments will change behaviour soon!
# It currently upgrades all formula but this will soon change to require '--all'.
from thefuck.specific.brew import brew_available

enabled_by_default = brew_available


def match(command):
    return command.script == 'brew upgrade'


def get_new_command(command):
    return command.script + ' --all'
