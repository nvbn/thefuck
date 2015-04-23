patterns = ['permission denied',
            'EACCES',
            'pkg: Insufficient privileges',
            'you cannot perform this operation unless you are root',
            'non-root users cannot',
            'Operation not permitted',
            'root privilege',
            'This command has to be run under the root user.',
            'This operation requires root.',
            'You need to be root to perform this command.']


def match(command, settings):
    for pattern in patterns:
        if pattern.lower() in command.stderr.lower():
            return True
    return False


def get_new_command(command, settings):
    return u'sudo {}'.format(command.script)
