from thefuck.specific.npm import npm_available, get_scripts
from thefuck.utils import for_app

enabled_by_default = npm_available


@for_app('npm')
def match(command):
    return ('Usage: npm <command>' in command.output
            and not any(part.startswith('ru') for part in command.script_parts)
            and command.script_parts[1] in get_scripts())


def get_new_command(command):
    parts = command.script_parts[:]
    parts.insert(1, 'run-script')
    return ' '.join(parts)
