import re


patterns = (
    r"mv: cannot move '[^']*' to '([^']*)': No such file or directory",
    r"cp: cannot create regular file '([^']*)': No such file or directory",
)


def match(command, settings):
    for pattern in patterns:
        if re.search(pattern, command.stderr):
            return True

    return False


def get_new_command(command, settings):
    for pattern in patterns:
        file = re.findall(pattern, command.stderr)

        if file:
            file = file[0]
            dir = file[0:file.rfind('/')]

            return 'mkdir -p {} && {}'.format(dir, command.script)
