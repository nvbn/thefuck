def match(command):
    return (
        command.script == 'git merge originmain'
    )


def get_new_command(command):
    return command.script.replace('originmain', 'origin/main', 1)
