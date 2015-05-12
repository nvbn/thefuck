def match(command, settings):
    return ('git' in command.script
            and 'Please commit or stash them.' in command.stderr)


def get_new_command(command, settings):
    return 'git stash && ' + command.script
