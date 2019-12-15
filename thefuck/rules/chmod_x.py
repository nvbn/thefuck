import os
from thefuck.shells import shell


def match(command):
    file_to_run = os.path.expanduser(command.script_parts[0])
    return (command.script.startswith('./')
            and 'permission denied' in command.output.lower()
            and os.path.exists(file_to_run)
            and not os.access(file_to_run, os.X_OK))


def get_new_command(command):
    return shell.and_(
        'chmod +x {}'.format(command.script_parts[0][2:]),
        command.script)
