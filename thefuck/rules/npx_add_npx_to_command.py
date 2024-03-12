import os
from os import path
from subprocess import Popen, PIPE
from thefuck.utils import memoize, eager, which, get_close_matches


priority = 900
enabled_by_default = bool(which('npx'))


def match(command):
    return \
        'not found' in command.output.lower() and \
        bool(get_matching_npm_executables_in_cd(command))


def get_new_command(command):
    skip = 1
    if command.script_parts[0] == 'npx':
        skip += 1
    script_parts = command.script_parts[skip:]
    return [
        ' '.join(['npx', e] + script_parts)
        for e in get_matching_npm_executables_in_cd(command)
    ]


def get_matching_npm_executables_in_cd(command):
    """Get all matching npm binaries in current npm bin folder."""
    npm_bin = get_npm_bin_folder()
    command_name = command.script_parts[0]
    if command_name == 'npx':
        command_name = command.script_parts[1]
    return get_matching_npm_executables(npm_bin, command_name)


def get_npm_bin_folder():
    """Get current npm bin folder."""
    proc = Popen(['npm', 'bin'], stdout=PIPE)
    return proc.stdout.readlines()[0].decode('utf-8').strip()


@memoize
@eager
def get_matching_npm_executables(bin, name):
    """Get all matching npm binaries."""
    if not path.isdir(bin):
        return []

    exact_command_path = path.join(bin, name)
    if path.isfile(exact_command_path):
        return [name]

    all_executables = [
        f for f in os.listdir(bin)
        if path.isfile(path.join(bin, f))
    ]
    return get_close_matches(name, all_executables)
