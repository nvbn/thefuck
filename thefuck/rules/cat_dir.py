import re


def match(command):
    return (
        command.script.startswith('cat') and
        re.match(r'cat: .+: Is a directory', command.output)
    )


def get_new_command(command):
    return re.sub(r'^cat', 'ls', command.script)
