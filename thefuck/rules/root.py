def match(command, settings):
    errors = ['Вы не можете выполнить эту операцию, не являясь суперпользователем (root).',
              'you cannot perform this operation unless you are root.']
    std_error = command.stderr
    return any(e in std_error for e in errors)


def get_new_command(command, settings):
    return 'sudo {}'.format(command.script)
