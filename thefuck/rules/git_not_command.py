import re
from thefuck.utils import (get_closest, git_support, replace_argument,
                           get_all_matched_commands)


@git_support
def match(command, settings):
    return (" is not a git command. See 'git --help'." in command.stderr
            and 'Did you mean' in command.stderr)


@git_support
def get_new_command(command, settings):
    broken_cmd = re.findall(r"git: '([^']*)' is not a git command",
                            command.stderr)[0]
    new_cmd = get_closest(broken_cmd,
                          get_all_matched_commands(command.stderr))
    return replace_argument(command.script, broken_cmd, new_cmd)

