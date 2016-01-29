import shlex
from thefuck.shells import shell
from thefuck.utils import for_app


@for_app('sed')
def match(command):
    return "unterminated `s' command" in command.stderr


def get_new_command(command):
    script = shlex.split(command.script)

    for (i, e) in enumerate(script):
        if e.startswith(('s/', '-es/')) and e[-1] != '/':
            script[i] += '/'

    return ' '.join(map(shell.quote, script))
