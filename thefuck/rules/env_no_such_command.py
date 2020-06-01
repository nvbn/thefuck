from subprocess import PIPE, Popen
from thefuck.utils import (for_app, replace_command)

@for_app('pyenv', 'rbenv', 'goenv', 'nodenv')
def match(command):
    return ('env' in command.script and 'no such command' in command.output)


def _get_operations(command):
    if 'env' in command.script_parts[0]:
        proc_env = Popen([str(command.script_parts[0]), 'commands'], stdout=PIPE)
    else:
        proc_env = Popen([str(command.script_parts[1]), 'commands'], stdout=PIPE)
    return [line.decode('utf-8').strip() for line in proc_env.stdout.readlines()]


@for_app('pyenv', 'rbenv', 'goenv', 'nodenv')
def get_new_command(command):
    if 'env' in command.script_parts[0]:
        invalid_operation = command.script_parts[1]
    else:
        invalid_operation = command.script_parts[0]

    return replace_command(command, invalid_operation, _get_operations(command))