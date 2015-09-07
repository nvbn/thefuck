from thefuck.specific.sudo import sudo_support

enabled_by_default = False


@sudo_support
def match(command):
    return ({'rm', '/'}.issubset(command.script.split())
            and '--no-preserve-root' not in command.script
            and '--no-preserve-root' in command.stderr)


@sudo_support
def get_new_command(command):
    return u'{} --no-preserve-root'.format(command.script)
