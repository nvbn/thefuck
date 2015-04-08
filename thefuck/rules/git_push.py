def match(command):
    return ('git' in command.script
            and 'push' in command.script
            and 'set-upstream' in command.stderr)


def get_new_command(command):
    return command.stderr.split('\n')[-3].strip()
