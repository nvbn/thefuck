import re
from thefuck.utils import for_app


@for_app('apt-get')
def match(command, settings):
    return command.script.startswith('apt-get search')


def get_new_command(command, settings):
    return re.sub(r'^apt-get', 'apt-cache', command.script)
