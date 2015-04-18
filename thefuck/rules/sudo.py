def match(command, settings):
    return ('permission denied' in command.stderr.lower()
            or 'EACCES' in command.stderr
            or 'error: you cannot perform this operation unless you are root.' in command.stderr
            or 'pkg: Insufficient privileges' in command.stderr)


def get_new_command(command, settings):
    return 'sudo {}'.format(command.script)
