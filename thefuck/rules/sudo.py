def match(command, settings):
    errors = ['вы не можете выполнить эту операцию, не являясь суперпользователем (root).',
              'you cannot perform this operation unless you are root.',
              'permission denied']
    std_error = command.stderr
    return any(e in std_error.lower() for e in errors) or 'EACCES' in std_error


def get_new_command(command, settings):
    return 'sudo {}'.format(command.script)
