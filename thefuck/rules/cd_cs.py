# Redirects cs to cd when there is a typo
# Due to the proximity of the keys - d and s, I found this to be a common problem for me
# > cs /etc/
# cs: command not found


def match(command):
    if command.script_parts[0] == 'cs':
        return True


def get_new_command(command):
    return 'cd' + ''.join(command.script[2:])


priority = 900
