def match(command):
    return 'permission denied' in command.stderr.lower()


def get_new_command(command):
    return 'sudo {}'.format(command.script)
