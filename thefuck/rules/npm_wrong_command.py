from thefuck.specific.npm import npm_available
from thefuck.utils import replace_argument, for_app, eager, get_closest
from thefuck.specific.sudo import sudo_support

enabled_by_default = npm_available


def _get_wrong_command(script_parts):
    commands = [part for part in script_parts[1:] if not part.startswith('-')]
    if commands:
        return commands[0]


@sudo_support
@for_app('npm')
def match(command):
    return (command.script_parts[0] == 'npm' and
            'where <command> is one of:' in command.stdout and
            _get_wrong_command(command.script_parts))


@eager
def _get_available_commands(stdout):
    commands_listing = False
    for line in stdout.split('\n'):
        if line.startswith('where <command> is one of:'):
            commands_listing = True
        elif commands_listing:
            if not line:
                break

            for command in line.split(', '):
                stripped = command.strip()
                if stripped:
                    yield stripped


def get_new_command(command):
    npm_commands = _get_available_commands(command.stdout)
    wrong_command = _get_wrong_command(command.script_parts)
    fixed = get_closest(wrong_command, npm_commands)
    return replace_argument(command.script, wrong_command, fixed)
