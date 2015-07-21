import re
from thefuck.utils import get_closest, git_support


@git_support
def match(command, settings):
    return (" is not a git command. See 'git --help'." in command.stderr
            and 'Did you mean' in command.stderr)


def _get_all_git_matched_commands(stderr):
    should_yield = False
    for line in stderr.split('\n'):
        if 'Did you mean' in line:
            should_yield = True
        elif should_yield and line:
            yield line.strip()


@git_support
def get_new_command(command, settings):
    broken_cmd = re.findall(r"git: '([^']*)' is not a git command",
                            command.stderr)[0]
    new_cmd = get_closest(broken_cmd,
                          _get_all_git_matched_commands(command.stderr))
    return command.script.replace(broken_cmd, new_cmd, 1)

