import re
from thefuck.utils import for_app


@for_app('heroku')
def match(command):
    return 'Run heroku _ to run' in command.stderr


def get_new_command(command):
    return re.findall('Run heroku _ to run ([^.]*)', command.stderr)[0]
