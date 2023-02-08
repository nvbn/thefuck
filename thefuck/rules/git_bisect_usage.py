import re

from thefuck.specific.git import git_support
from thefuck.utils import replace_command


@git_support
def match(command):
    return ('bisect' in command.script_parts and
            'usage: git bisect' in command.output)


@git_support
def get_new_command(command):
    broken = re.findall(r'git bisect ([^ $]*).*', command.script)[0]
    usage = re.findall(r'usage: git bisect \[([^\]]+)\]', command.output)[0]
    return replace_command(command, broken, usage.split('|'))
