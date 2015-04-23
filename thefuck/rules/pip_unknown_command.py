import re


def match(command, settings):
    return ('pip' in command.script and
            'unknown command' in command.stderr and
            'maybe you meant' in command.stderr)


def get_new_command(command, settings):
    broken_cmd = re.findall(r'ERROR: unknown command \"([a-z]+)\"',
                            command.stderr)[0]
    new_cmd = re.findall(r'maybe you meant \"([a-z]+)\"', command.stderr)[0]

    return command.script.replace(broken_cmd, new_cmd, 1)
