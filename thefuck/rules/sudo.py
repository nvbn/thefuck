patterns = ['permission denied',
            'EACCES',
            'pkg: Insufficient privileges',
            'you cannot perform this operation unless you are root',
            'non-root users cannot',
            'Operation not permitted',
            'root privilege',
            'This command has to be run under the root user.',
            'This operation requires root.',
            'You need to be root to perform this command.',
            'requested operation requires superuser privilege',
            'must be run as root',
            'must be superuser',
            'Need to be root']


def match(command, settings):
    for pattern in patterns:
        if pattern.lower() in command.stderr.lower()\
                or pattern.lower() in command.stdout.lower():
            return True
    return False


def get_new_command(command, settings):
    return u'sudo {}'.format(command.script)
