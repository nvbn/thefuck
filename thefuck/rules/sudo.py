def match(command, settings):
    return ('permission denied' in command.stderr.lower()
            or 'EACCES' in command.stderr)


def get_new_command(command, settings):
    return 'sudo {}'.format(command.script)
