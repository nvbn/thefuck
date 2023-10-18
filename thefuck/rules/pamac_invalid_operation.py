import subprocess
from thefuck.utils import for_app, eager, replace_command

@for_app('pamac')
def match(command):
    return "Available actions:" in command.output


@eager
def _parse_pamac_operations(help_text_lines):
    is_commands_list = False
    for line in help_text_lines:
        line = line.decode().strip()
        if is_commands_list and line:
            yield line.split()[1].split(',')[0]
        elif line.startswith('Available actions:'):
            is_commands_list = True

def _get_operations(app):
    proc = subprocess.Popen([app, '--help'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    lines = proc.stdout.readlines()

    if app == 'pamac':
        return _parse_pamac_operations(lines)


def get_new_command(command):
    invalid_operation = command.script.split()[1]

    if invalid_operation == 'uninstall':
        return [command.script.replace('uninstall', 'remove')]

    else:
        operations = _get_operations(command.script_parts[0])
        return replace_command(command, invalid_operation, operations)
