from thefuck import shells
from thefuck.utils import memoize


def get_packages(command):
    splitted_command = command.script.split()
    if splitted_command[0] == 'sudo':
        return splitted_command[3:]
    return splitted_command[2:]


def match(command):
    typos = ('dfn install', 'dnf istall', 'dfn istall')
    patterns = ("not found", "No such command")
    stderr = command.stderr

    found_pattern = any(pattern in stderr for pattern in patterns)
    found_typo = any(typo in command.script for typo in typos)
    return  found_pattern and found_typo


def get_new_command(command):
    packages = get_packages(command)
    return 'sudo dnf install {}'.format(' '.join(packages))
