import re
from subprocess import Popen, PIPE
from thefuck.utils import for_app, replace_command, cache, eager


@for_app('react-native')
def match(command):
    return re.findall(r"Unrecognized command '.*'", command.output)


@cache('package.json')
@eager
def _get_commands():
    proc = Popen(['react-native', '--help'], stdout=PIPE)
    should_yield = False
    for line in proc.stdout.readlines():
        line = line.decode().strip()

        if not line:
            continue

        if 'Commands:' in line:
            should_yield = True
            continue

        if should_yield:
            yield line.split(' ')[0]


def get_new_command(command):
    misspelled_command = re.findall(r"Unrecognized command '(.*)'",
                                    command.output)[0]
    commands = _get_commands()
    return replace_command(command, misspelled_command, commands)
