import re
import subprocess

from thefuck.specific.dnf import dnf_available
from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, replace_command

regex = re.compile(r'No such command: (.*)\.')


@sudo_support
@for_app('dnf')
def match(command):
    return 'no such command' in command.output.lower()


def _parse_operations(help_text_lines):
    operation_regex = re.compile(r'^([a-z-]+) +', re.MULTILINE)
    return operation_regex.findall(help_text_lines)


def _get_operations():
    proc = subprocess.Popen(["dnf", '--help'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    lines = proc.stdout.read().decode("utf-8")

    return _parse_operations(lines)


@sudo_support
def get_new_command(command):
    misspelled_command = regex.findall(command.output)[0]
    return replace_command(command, misspelled_command, _get_operations())


enabled_by_default = dnf_available
