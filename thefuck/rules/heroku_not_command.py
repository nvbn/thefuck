import re
from thefuck.utils import replace_command, for_app


@for_app('heroku')
def match(command, settings):
    return 'is not a heroku command' in command.stderr and \
           'Perhaps you meant' in command.stderr


def _get_suggests(stderr):
    for line in stderr.split('\n'):
        if 'Perhaps you meant' in line:
            return re.findall(r'`([^`]+)`', line)


def get_new_command(command, settings):
    wrong = re.findall(r'`(\w+)` is not a heroku command', command.stderr)[0]
    return replace_command(command, wrong, _get_suggests(command.stderr))
