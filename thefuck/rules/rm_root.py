enabled_by_default = False


def match(command, settings):
    return ({'rm', '/'}.issubset(command.script.split())
            and '--no-preserve-root' not in command.script
            and '--no-preserve-root' in command.stderr)


def get_new_command(command, settings):
    return u'{} --no-preserve-root'.format(command.script)
