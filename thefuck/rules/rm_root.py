def match(command, settings):
    return ('/' in command.script
            and '--no-preserve-root' not in command.script
            and '--no-preserve-root' in command.stderr)


def get_new_command(command, settings):
    return '{} --no-preserve-root'.format(command.script)
