import os
from thefuck.specific.sudo import sudo_support


@sudo_support
def match(command):
    return os.path.exists(command.script.split()[0]) \
        and 'command not found' in command.stderr


@sudo_support
def get_new_command(command):
    return u'./{}'.format(command.script)
