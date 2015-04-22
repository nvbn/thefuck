import re

patterns = [
    r'WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!',
    r'WARNING: POSSIBLE DNS SPOOFING DETECTED!',
    r"Warning: the \S+ host key for '([^']+)' differs from the key for the IP address '([^']+)'",
]
offending_pattern = re.compile(
    r'(?:Offending (?:key for IP|\S+ key)|Matching host key) in ([^:]+):(\d+)',
    re.MULTILINE)

commands = ['ssh', 'scp']


def match(command, settings):
    if not command.script:
        return False
    if not command.script.split()[0] in commands:
        return False
    if not any([re.findall(pattern, command.stderr) for pattern in patterns]):
        return False
    return True


def remove_offending_keys(command, settings):
    offending = offending_pattern.findall(command.stderr)
    for filepath, lineno in offending:
        with open(filepath, 'r') as fh:
            lines = fh.readlines()
            del lines[int(lineno) - 1]
        with open(filepath, 'w') as fh:
            fh.writelines(lines)


def get_new_command(command, settings):
    remove_offending_keys(command, settings)
    return command.script
