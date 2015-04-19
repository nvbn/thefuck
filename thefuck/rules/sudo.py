patterns = ['permission denied',
            'EACCES',
            'pkg: Insufficient privileges',
            'you cannot perform this operation unless you are root',
            'non-root users cannot',
            'Operation not permitted']


def match(command, settings):
    for pattern in patterns:
        if pattern.lower() in command.stderr.lower():
            return True
    return False


def get_new_command(command, settings):
    return 'sudo {}'.format(command.script)
