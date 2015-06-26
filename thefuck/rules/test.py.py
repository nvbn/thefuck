def match(command, settings):
    return command.script == 'test.py' and 'not found' in command.stderr


def get_new_command(command, settings):
    return 'py.test'


# make it come before the python_command rule
priority = 900
