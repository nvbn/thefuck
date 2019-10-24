from thefuck.specific.sudo import sudo_support

enabled_by_default = False


@sudo_support
def match(command):
    return (command.script_parts
            and {'rm', '/'}.issubset(command.script_parts))


@sudo_support
def get_new_command(command):
    return u'echo "I\'m saving your life. Thank me later"'
