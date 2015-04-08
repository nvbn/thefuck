def match(command):
    return ('permission denied' in command.stderr.lower()
            or 'EACCES' in command.stderr)


def get_new_command(command):
    return 'sudo {}'.format(command.script)
