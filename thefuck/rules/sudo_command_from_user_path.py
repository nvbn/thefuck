import re
from thefuck.utils import for_app, which, replace_argument


def _get_command_name(command):
    found = re.findall(r'sudo: (.*): command not found', command.output)
    if found:
        return found[0]


@for_app('sudo')
def match(command):
    if 'command not found' in command.output:
        command_name = _get_command_name(command)
        return which(command_name)


def get_new_command(command):
    command_name = _get_command_name(command)
    return replace_argument(command.script, command_name,
                            u'env "PATH=$PATH" {}'.format(command_name))
