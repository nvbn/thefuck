import os
from thefuck.shells import shell


def match(command):
    return (command.script.startswith('./')
            and 'permission denied' in command.stderr.lower()
            and os.path.exists(command.script_parts[0])
            and not os.access(command.script_parts[0], os.X_OK))


def get_new_command(command):
    return shell.and_(
        'chmod +x {}'.format(command.script_parts[0][2:]),
        command.script)
