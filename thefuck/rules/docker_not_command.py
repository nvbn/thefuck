from itertools import dropwhile, takewhile, islice
import re
import subprocess
from thefuck.utils import replace_command, for_app, which, cache
from thefuck.specific.sudo import sudo_support


@sudo_support
@for_app('docker')
def match(command):
    return 'is not a docker command' in command.output


def get_docker_commands():
    proc = subprocess.Popen('docker', stdout=subprocess.PIPE)
    lines = [line.decode('utf-8') for line in proc.stdout.readlines()]
    lines = dropwhile(lambda line: not line.startswith('Commands:'), lines)
    lines = islice(lines, 1, None)
    lines = list(takewhile(lambda line: line != '\n', lines))
    return [line.strip().split(' ')[0] for line in lines]


if which('docker'):
    get_docker_commands = cache(which('docker'))(get_docker_commands)


@sudo_support
def get_new_command(command):
    wrong_command = re.findall(
        r"docker: '(\w+)' is not a docker command.", command.output)[0]
    return replace_command(command, wrong_command, get_docker_commands())
