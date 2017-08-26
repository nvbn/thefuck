import re
from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('push' in command.script
            and 'set-upstream' in command.stderr)


def _get_upstream_option_index(command_parts):
    if '--set-upstream' in command_parts:
        return command_parts.index('--set-upstream')
    elif '-u' in command_parts:
        return command_parts.index('-u')
    else:
        return None


@git_support
def get_new_command(command):
    # If --set-upstream or -u are passed, remove it and its argument. This is
    # because the remaining arguments are concatenated onto the command suggested
    # by git, which includes --set-upstream and its argument
    command_parts = command.script_parts[:]
    upstream_option_index = _get_upstream_option_index(command_parts)

    if upstream_option_index is not None:
        command_parts.pop(upstream_option_index)

        # In case of `git push -u` we don't have next argument:
        if len(command_parts) > upstream_option_index:
            command_parts.pop(upstream_option_index)

    arguments = re.findall(r'git push (.*)', command.stderr)[0].strip()
    return replace_argument(" ".join(command_parts), 'push',
                            'push {}'.format(arguments))
