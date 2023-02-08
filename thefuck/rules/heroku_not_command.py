import re

from thefuck.utils import for_app


@for_app('heroku')
def match(command):
    return 'Run heroku _ to run' in command.output


def get_new_command(command):
    return re.findall('Run heroku _ to run ([^.]*)', command.output)[0]
