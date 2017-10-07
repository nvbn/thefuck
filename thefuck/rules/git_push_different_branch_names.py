import re
from thefuck.specific.git import git_support


@git_support
def match(command):
    return "git push" in command.script and "The upstream branch of your current branch does not match" in command.output


@git_support
def get_new_command(command):
    return re.findall(r'^ +(git push [^\s]+ [^\s]+)', command.output, re.MULTILINE)[0]


enabled_by_default = True
