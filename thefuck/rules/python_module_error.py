import re
from thefuck.shells import shell

MISSING_MODULE = r"ModuleNotFoundError: No module named '([^']+)'"


def match(command):
    return "ModuleNotFoundError: No module named '" in command.output


def get_new_command(command):
    missing_module = re.findall(MISSING_MODULE, command.output)[0]
    return shell.and_("pip install {}".format(missing_module), command.script)
