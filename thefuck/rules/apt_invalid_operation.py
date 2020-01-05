import subprocess
from thefuck.specific.apt import apt_available
from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, eager, replace_command

enabled_by_default = apt_available


@sudo_support
@for_app('apt', 'apt-get', 'apt-cache')
def match(command):
    return 'E: Invalid operation' in command.output


@eager
def _parse_apt_operations(help_text_lines):
    is_commands_list = False
    for line in help_text_lines:
        line = line.decode().strip()
        if is_commands_list and line:
            yield line.split()[0]
        elif line.startswith('Basic commands:') \
                or line.startswith('Most used commands:'):
            is_commands_list = True


@eager
def _parse_apt_get_and_cache_operations(help_text_lines):
    is_commands_list = False
    for line in help_text_lines:
        line = line.decode().strip()
        if is_commands_list:
            if not line:
                return

            yield line.split()[0]
        elif line.startswith('Commands:') \
                or line.startswith('Most used commands:'):
            is_commands_list = True


def _get_operations(app):
    proc = subprocess.Popen([app, '--help'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    lines = proc.stdout.readlines()

    if app == 'apt':
        return _parse_apt_operations(lines)
    else:
        return _parse_apt_get_and_cache_operations(lines)


@sudo_support
def get_new_command(command):
    invalid_operation = command.output.split()[-1]

    if invalid_operation == 'uninstall':
        return [command.script.replace('uninstall', 'remove')]

    else:
        operations = _get_operations(command.script_parts[0])
        return replace_command(command, invalid_operation, operations)
