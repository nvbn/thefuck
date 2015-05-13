def match(command, settings):
    # catches "Please commit or stash them" and "Please, commit your changes or
    # stash them before you can switch branches."
    return 'git' in command.script and 'or stash them' in command.stderr


def get_new_command(command, settings):
    return 'git stash && ' + command.script
