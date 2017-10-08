import re

from thefuck.specific.git import git_support


@git_support
def match(command):
    return "remote delete" in command.script


@git_support
def get_new_command(command):
    return re.sub(r"delete", "remove", command.script, 1)
