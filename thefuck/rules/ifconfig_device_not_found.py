import subprocess
from thefuck.utils import for_app, replace_command, eager
import sys

@for_app('ifconfig')
def match(command):
    return 'error fetching interface information: Device not found' \
           in command.stderr


@eager
def _get_possible_interfaces():
    proc = subprocess.Popen(['ifconfig', '-a'], stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
        line = line.decode()
        if line and line != '\n' and not line.startswith(' '):
            yield line.split(' ')[0]


def get_new_command(command):
    interface = command.stderr.split(' ')[0][:-1]
    possible_interfaces = _get_possible_interfaces()
    return replace_command(command, interface, possible_interfaces)


