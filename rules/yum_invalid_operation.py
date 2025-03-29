import subprocess
from itertools import dropwhile, islice, takewhile

from thefuck.specific.sudo import sudo_support
from thefuck.specific.yum import yum_available
from thefuck.utils import for_app, replace_command, which, cache

enabled_by_default = yum_available


@sudo_support
@for_app('yum')
def match(command):
    return 'No such command: ' in command.output


def _get_operations():
    proc = subprocess.Popen('yum', stdout=subprocess.PIPE)

    lines = proc.stdout.readlines()
    lines = [line.decode('utf-8') for line in lines]
    lines = dropwhile(lambda line: not line.startswith("List of Commands:"), lines)
    lines = islice(lines, 2, None)
    lines = list(takewhile(lambda line: line.strip(), lines))
    return [line.strip().split(' ')[0] for line in lines]


if which('yum'):
    _get_operations = cache(which('yum'))(_get_operations)


@sudo_support
def get_new_command(command):
    invalid_operation = command.script_parts[1]

    if invalid_operation == 'uninstall':
        return [command.script.replace('uninstall', 'remove')]

    return replace_command(command, invalid_operation, _get_operations())
