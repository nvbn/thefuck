import re
from thefuck.specific.nix import nix_available
from thefuck.shells import shell

regex = re.compile(r'nix-env -iA ([^\s]*)')
enabled_by_default = nix_available


def match(command):
    return regex.findall(command.output)


def get_new_command(command):
    name = regex.findall(command.output)[0]
    return shell.and_('nix-env -iA {}'.format(name), command.script)
