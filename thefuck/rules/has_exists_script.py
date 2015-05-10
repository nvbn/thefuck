import os
from thefuck.utils import sudo_support


@sudo_support
def match(command, settings):
    return os.path.exists(command.script.split()[0]) \
        and 'command not found' in command.stderr


@sudo_support
def get_new_command(command, settings):
    return u'./{}'.format(command.script)

