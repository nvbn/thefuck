import re
from thefuck.utils import get_all_matched_commands, replace_command
from thefuck.specific.git import git_support


@git_support
def match(command):
    return (" is not a git command. See 'git --help'." in command.output
            and ('The most similar command' in command.output
                 or 'Did you mean' in command.output))


@git_support
def get_new_command(command):
    broken_cmd = re.findall(r"git: '([^']*)' is not a git command",
                            command.output)[0]
    matched = get_all_matched_commands(command.output, ['The most similar command', 'Did you mean'])
    return replace_command(command, broken_cmd, matched)
