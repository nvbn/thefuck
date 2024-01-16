import re
from thefuck.utils import get_all_matched_commands, replace_command
from thefuck.specific.git import git_support


COMMON_TYPOS = {
    'copy': ['branch'],
    'list': ['branch'],
    'lock': ['log'],
    'update': ['fetch', 'fetch --all', 'fetch --all --tags', 'remote update'],
}


@git_support
def match(command):
    return (" is not a git command. See 'git --help'." in command.output
            and ('The most similar command' in command.output
                 or 'Did you mean' in command.output))


@git_support
def get_new_command(command):
    broken_cmd = re.findall(r"git: '([^']*)' is not a git command",
                            command.output)[0]
    # check if the broken_cmd exists in COMMON_TYPOS
    if broken_cmd in COMMON_TYPOS:
        matched = COMMON_TYPOS[broken_cmd]
    else:
        matched = get_all_matched_commands(command.output, ['The most similar command', 'Did you mean'])
    return replace_command(command, broken_cmd, matched)
