import re
from thefuck.utils import for_app, replace_command


@for_app('react-native')
def match(command):
    return re.match(r'Command `.*` unrecognized', command.stderr)


def get_new_command(command):
    misspelled_command = re.findall(r'Command `(.*)` unrecognized',
                                    command.stderr)[0]
    commands = re.findall(r'  - (.*): .*\n', command.stdout)
    return replace_command(command, misspelled_command, commands)
