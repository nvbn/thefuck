import re
from thefuck.shells import shell
from thefuck.utils import for_app


@for_app('touch')
def match(command):
    return 'No such file or directory' in command.stderr


def get_new_command(command):
    path = re.findall(r"touch: cannot touch '(.+)/.+':", command.stderr)[0]
    return shell.and_(u'mkdir -p {}'.format(path), command.script)
