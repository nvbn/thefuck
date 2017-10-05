import re
from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return "git push" in command.script and "The upstream branch of your current branch does not match" in command.output


@git_support
def _parse_git_output(output):
    regex = re.compile(r'^ +(git push [^\s]+ [^\s]+)', re.MULTILINE)
    return regex.findall(output)[0]


@git_support
def get_new_command(command):
    return replace_argument(command.script, "delete", "remove")
