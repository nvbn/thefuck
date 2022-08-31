import re
from theheck.shells import shell
from theheck.specific.git import git_support


@git_support
def match(command):
    return bool(re.search(r"src refspec \w+ does not match any", command.output))


def get_new_command(command):
    return shell.and_('git commit -m "Initial commit"', command.script)
