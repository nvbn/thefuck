import re
from subprocess import Popen, PIPE
from thefuck.utils import for_app, memoize, eager


@memoize
@eager
def get_scripts():
    proc = Popen(['npm', 'run-script'], stdout=PIPE)
    should_yeild = False
    for line in proc.stdout.readlines():
        line = line.decode()
        if 'available via `npm run-script`:' in line:
            should_yeild = True
            continue

        if should_yeild and re.match(r'^  [^ ]+', line):
            yield line.strip().split(' ')[0]


@for_app('npm')
def match(command):
    return ('Usage: npm <command>' in command.stdout
            and not any(part.startswith('ru') for part in command.script_parts)
            and command.script_parts[1] in get_scripts())


def get_new_command(command):
    parts = command.script_parts[:]
    parts.insert(1, 'run-script')
    return ' '.join(parts)
