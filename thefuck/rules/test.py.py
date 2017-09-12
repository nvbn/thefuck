def match(command):
    return command.script == 'test.py' and 'not found' in command.output


def get_new_command(command):
    return 'py.test'


# make it come before the python_command rule
priority = 900
