from thefuck.utils import eager, replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return (
        "commit" in command.script_parts
        and "no changes added to commit" in command.output
    )


@eager
@git_support
def get_new_command(command):
    for opt in ("-a", "-p"):
        yield replace_argument(command.script, "commit", "commit {}".format(opt))
