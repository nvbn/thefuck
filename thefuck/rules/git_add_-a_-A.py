def match(command):
    return command.script == 'git add -a'


def get_new_command(command):
    return 'git add -A'
