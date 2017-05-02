patterns = ['docker.sock']


def match(command, settings):
    for pattern in patterns:
        if pattern.lower() in command.stderr.lower()\
                or pattern.lower() in command.stdout.lower():
            return True
    return False


def get_new_command(command, settings):
    return u'sudo {}'.format(command.script)
