def match(command):
    return command.script == 'add'


def get_new_command(command):
    return 'git add -A'
