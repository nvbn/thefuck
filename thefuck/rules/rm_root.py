from thefuck.specific.sudo import sudo_support

enabled_by_default = False


@sudo_support
def match(command):
    return (command.script_parts
            and {'rm', '/'}.issubset(command.script_parts)
            and '--no-preserve-root' not in command.script
            and '--no-preserve-root' in command.stderr)


@sudo_support
def get_new_command(command):
    return u'{} --no-preserve-root'.format(command.script)
