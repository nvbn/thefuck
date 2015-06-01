def match(command, settings):
    return command.script.startswith('git d')


def get_new_command(command, settings):
    return '{} --staged'.format(command.script)
