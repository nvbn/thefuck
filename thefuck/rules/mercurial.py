import re
from thefuck.utils import get_closest, for_app


def extract_possibilities(command):
    possib = re.findall(r'\n\(did you mean one of ([^\?]+)\?\)', command.output)
    if possib:
        return possib[0].split(', ')
    possib = re.findall(r'\n    ([^$]+)$', command.output)
    if possib:
        return possib[0].split(' ')
    return possib


@for_app('hg')
def match(command):
    return ('hg: unknown command' in command.output
            and '(did you mean one of ' in command.output
            or "hg: command '" in command.output
            and "' is ambiguous:" in command.output)


def get_new_command(command):
    script = command.script_parts[:]
    possibilities = extract_possibilities(command)
    script[1] = get_closest(script[1], possibilities)
    return ' '.join(script)
