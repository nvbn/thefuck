import re
from thefuck.utils import get_closest


def extract_possibilities(command):
    possib = re.findall(r'\n\(did you mean one of ([^\?]+)\?\)', command.stderr)
    if possib:
        return possib[0].split(', ')
    possib = re.findall(r'\n    ([^$]+)$', command.stderr)
    if possib:
        return possib[0].split(' ')
    return possib


def match(command, settings):
    return (command.script.startswith('hg ')
            and ('hg: unknown command' in command.stderr
                 and '(did you mean one of ' in command.stderr
                 or "hg: command '" in command.stderr
                 and "' is ambiguous:" in command.stderr
                 )
            )


def get_new_command(command, settings):
    script = command.script.split(' ')
    possibilities = extract_possibilities(command)
    script[1] = get_closest(script[1], possibilities)
    return ' '.join(script)
