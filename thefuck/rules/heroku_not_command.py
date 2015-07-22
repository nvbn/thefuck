import re
from thefuck.utils import get_closest


def match(command, settings):
    return command.script.startswith('heroku') and \
           'is not a heroku command' in command.stderr and \
           'Perhaps you meant' in command.stderr


def _get_suggests(stderr):
    for line in stderr.split('\n'):
        if 'Perhaps you meant' in line:
            return re.findall(r'`([^`]+)`', line)


def get_new_command(command, settings):
    wrong = re.findall(r'`(\w+)` is not a heroku command', command.stderr)[0]
    correct = get_closest(wrong, _get_suggests(command.stderr))
    return command.script.replace(' {}'.format(wrong), ' {}'.format(correct), 1)
