import re
from thefuck.shells import shell
from thefuck.utils import for_app
from thefuck.utils import which


@for_app('mdt')
def match(command):
    return "Unknown command" in command.output and "try 'mdt help'" in command.output


def get_new_command(command):
    #mdt_commands = []
    return "mdt" + "shell"
