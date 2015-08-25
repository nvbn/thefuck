from functools import wraps
import re
from shlex import split
from ..types import Command
from ..utils import quote


def git_support(fn):
    """Resolves git aliases and supports testing for both git and hub."""
    @wraps(fn)
    def wrapper(command, settings):
        # supports GitHub's `hub` command
        # which is recommended to be used with `alias git=hub`
        # but at this point, shell aliases have already been resolved
        is_git_cmd = command.script.startswith(('git', 'hub'))

        if not is_git_cmd:
            return False

        # perform git aliases expansion
        if 'trace: alias expansion:' in command.stderr:
            search = re.search("trace: alias expansion: ([^ ]*) => ([^\n]*)",
                               command.stderr)
            alias = search.group(1)

            # by default git quotes everything, for example:
            #     'commit' '--amend'
            # which is surprising and does not allow to easily test for
            # eg. 'git commit'
            expansion = ' '.join(map(quote, split(search.group(2))))
            new_script = command.script.replace(alias, expansion)

            command = Command._replace(command, script=new_script)

        return fn(command, settings)

    return wrapper
