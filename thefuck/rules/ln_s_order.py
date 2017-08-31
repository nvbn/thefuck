import os
from thefuck.specific.sudo import sudo_support


def _get_destination(script_parts):
    """When arguments order is wrong first argument will be destination."""
    for part in script_parts:
        if part not in {'ln', '-s', '--symbolic'} and os.path.exists(part):
            return part


@sudo_support
def match(command):
    return (command.script_parts[0] == 'ln'
            and {'-s', '--symbolic'}.intersection(command.script_parts)
            and 'File exists' in command.output
            and _get_destination(command.script_parts))


@sudo_support
def get_new_command(command):
    destination = _get_destination(command.script_parts)
    parts = command.script_parts[:]
    parts.remove(destination)
    parts.append(destination)
    return ' '.join(parts)
