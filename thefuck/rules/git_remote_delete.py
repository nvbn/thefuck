from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return "git remote delete" in command.script


@git_support
def get_new_command(command):
    return replace_argument(command.script, "delete", "remove")


enabled_by_default = True
