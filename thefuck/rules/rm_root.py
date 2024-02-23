import sys
from warnings import warn
from thefuck.specific.sudo import sudo_support

enabled_by_default = False


@sudo_support
def match(command):
    return (command.script_parts
            and {'rm', '/'}.issubset(command.script_parts))


def get_new_command(command):
    return '{} {} {}'.format(command.script_parts[0], '-rf', ' '.join(command.script_parts[1:]))


def side_effect(old_cmd, command):
    warn("DANGER!!! THIS MAY DESTROY YOUR SYSTEM! ARE YOU SURE? (y/N): ")
    try:
        input = raw_input
    except NameError:
        pass
    reply = input().strip().lower()  # raw_input should be used in Python 2
    if not reply or reply[0] != "y":
        sys.exit(0)
