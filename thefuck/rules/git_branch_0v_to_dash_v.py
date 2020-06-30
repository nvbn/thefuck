from thefuck.shells import shell
from thefuck.specific.git import git_support
from thefuck.utils import memoize

'''
keys are fatfingered entry, values are two-element tuples
where the first element is "the fix" and the second element
is "what you meant to do
 '''
# clunky when there's only one key, but as others get added, I _think_
# this will be cleaner
flags_and_their_fixes = dict()
flags_and_their_fixes["v"] = ('git branch -D 0v', 'git branch -v')


@memoize
def _supported_flag_fix(command):
    flag = command.script_parts[2:][0]

    if len(flag) == 2 and flag.startswith("0"):
        return flags_and_their_fixes[flag[1]]
    else:
        return None


@git_support
def match(command):
    return (command.script_parts
            and command.script_parts[1] == 'branch'
            and _supported_flag_fix(command) is not None)


@git_support
def get_new_command(command):
    fix_parts = _supported_flag_fix(command)
    return shell.and_(fix_parts[0], fix_parts[1])
