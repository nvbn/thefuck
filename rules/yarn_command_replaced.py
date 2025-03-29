import re
from thefuck.utils import for_app

regex = re.compile(r'Run "(.*)" instead')


@for_app('yarn', at_least=1)
def match(command):
    return regex.findall(command.output)


def get_new_command(command):
    return regex.findall(command.output)[0]
