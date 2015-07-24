patterns = ['permission denied',
            'EACCES',
            'pkg: Insufficient privileges',
            'you cannot perform this operation unless you are root',
            'non-root users cannot',
            'Operation not permitted',
            'root privilege',
            'This command has to be run under the root user.',
            'This operation requires root.',
            'requested operation requires superuser privilege',
            'must be run as root',
            'must be superuser',
            'must be root',
            'need to be root',
            'need root',
            'only root can ',
            'You don\'t have access to the history DB.',
            'authentication is required']


def match(command, settings):
    for pattern in patterns:
        if pattern.lower() in command.stderr.lower()\
                or pattern.lower() in command.stdout.lower():
            return True
    return False


def get_new_command(command, settings):
    return u'sudo {}'.format(command.script)
