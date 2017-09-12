import re
from thefuck.specific.git import git_support

fix = u'git commit -m "Initial commit." && {command}'
refspec_does_not_match = re.compile(r'src refspec \w+ does not match any\.')


@git_support
def match(command):
    return bool(refspec_does_not_match.search(command.output))


def get_new_command(command):
    return fix.format(command=command.script)
