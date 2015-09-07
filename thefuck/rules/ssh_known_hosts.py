import re
from thefuck.utils import for_app

commands = ('ssh', 'scp')


@for_app(*commands)
def match(command):
    if not command.script:
        return False
    if not command.script.startswith(commands):
        return False

    patterns = (
        r'WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!',
        r'WARNING: POSSIBLE DNS SPOOFING DETECTED!',
        r"Warning: the \S+ host key for '([^']+)' differs from the key for the IP address '([^']+)'",
    )

    return any(re.findall(pattern, command.stderr) for pattern in patterns)


def get_new_command(command):
    return command.script


def side_effect(old_cmd, command):
    offending_pattern = re.compile(
        r'(?:Offending (?:key for IP|\S+ key)|Matching host key) in ([^:]+):(\d+)',
        re.MULTILINE)
    offending = offending_pattern.findall(old_cmd.stderr)
    for filepath, lineno in offending:
        with open(filepath, 'r') as fh:
            lines = fh.readlines()
            del lines[int(lineno) - 1]
        with open(filepath, 'w') as fh:
            fh.writelines(lines)
