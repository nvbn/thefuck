import re
from thefuck.utils import replace_argument
from thefuck.specific.git import git_support


@git_support
def match(command):
    return ('push' in command.script_parts
            and 'git push --set-upstream' in command.output)


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
    else:
        # the only non-qualified permitted options are the repository and refspec; git's
        # suggestion include them, so they won't be lost, but would be duplicated otherwise.
        push_idx = command_parts.index('push') + 1
        while len(command_parts) > push_idx and command_parts[len(command_parts) - 1][0] != '-':
            command_parts.pop(len(command_parts) - 1)

    arguments = re.findall(r'git push (.*)', command.output)[-1].replace("'", r"\'").strip()
    return replace_argument(" ".join(command_parts), 'push',
                            'push {}'.format(arguments))
