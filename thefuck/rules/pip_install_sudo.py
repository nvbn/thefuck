import re
from thefuck.utils import sudo_support


def match(command, settings):
    return (('pip' in command.script and 'install' in command.script) and
            'failed with error code 1' in command.stderr and
            ('Errno 13' in command.stdout or
             'Permission denied' in command.stdout))


def get_new_command(command, settings):
    return u'sudo {}'.format(command.script)
