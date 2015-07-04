import shlex
from thefuck.utils import quote


def match(command, settings):
    return ('sed' in command.script
            and "unterminated `s' command" in command.stderr)


def get_new_command(command, settings):
    script = shlex.split(command.script)

    for (i, e) in enumerate(script):
        if e.startswith(('s/', '-es/')) and e[-1] != '/':
            script[i] += '/'

    return ' '.join(map(quote, script))
