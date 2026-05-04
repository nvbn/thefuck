from thefuck.shells import shell

patterns = ['permission denied',
            'eacces',
            'pkg: insufficient privileges',
            'you cannot perform this operation unless you are root',
            'non-root users cannot',
            'operation not permitted',
            'not super-user',
            'superuser privilege',
            'root privilege',
            'this command has to be run under the root user.',
            'this operation requires root.',
            'requested operation requires superuser privilege',
            'must be run as root',
            'must run as root',
            'must be superuser',
            'must be root',
            'need to be root',
            'need root',
            'needs to be run as root',
            'only root can ',
            'you don\'t have access to the history db.',
            'authentication is required',
            'edspermissionerror',
            'you don\'t have write permissions',
            'use `sudo`',
            'sudorequirederror',
            'error: insufficient privileges',
            'updatedb: can not open a temporary file']


def match(command):
    if command.script_parts and command.script_parts[0] == 'sudo':
        return False

    for pattern in patterns:
        if pattern in command.output.lower():
            return True
    return False


def _is_and_command(command):
    return shell.and_('') in command.script


def get_new_command(command):
    if _is_and_command(command):
        return u'sudo sh -c "{}"'.format(" ".join([part for part in command.script_parts if part != "sudo"]))
    elif '>' in command.script:
        return u'sudo sh -c "{}"'.format(command.script.replace('"', '\\"'))
    else:
        return u'sudo {}'.format(command.script)