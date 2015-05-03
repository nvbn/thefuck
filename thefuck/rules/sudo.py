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
            'Need to be root',
            '\u0437\u0430\u043F\u0440\u043E\u0448\u0435\u043D\u043D\u0430\u044F \u043E\u043F\u0435\u0440\u0430\u0446\u0438\u044F \u0442\u0440\u0435\u0431\u0443\u0435\u0442 \u043F\u0440\u0438\u0432\u0438\u043B\u0435\u0433\u0438\u0439 \u0441\u0443\u043F\u0435\u0440\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u0435\u043B\u044F']


def match(command, settings):
    for pattern in patterns:
        if pattern.lower() in command.stderr.lower()\
                or pattern.lower() in command.stdout.lower():
            return True
    return False


def get_new_command(command, settings):
    return u'sudo {}'.format(command.script)
