import re
import subprocess
from thefuck.utils import for_app, eager, replace_command


@for_app('gem')
def match(command):
    return ('ERROR:  While executing gem ... (Gem::CommandLineError)'
            in command.stderr
            and 'Unknown command' in command.stderr)


def _get_unknown_command(command):
    return re.findall(r'Unknown command (.*)$', command.stderr)[0]


@eager
def _get_all_commands():
    proc = subprocess.Popen(['gem', 'help', 'commands'],
                            stdout=subprocess.PIPE)

    for line in proc.stdout.readlines():
        line = line.decode()

        if line.startswith('    '):
            yield line.strip().split(' ')[0]


def get_new_command(command):
    unknown_command = _get_unknown_command(command)
    all_commands = _get_all_commands()
    return replace_command(command, unknown_command, all_commands)
