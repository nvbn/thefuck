import re
from thefuck import utils, shells


@utils.git_support
def match(command, settings):
    return ('did not match any file(s) known to git.' in command.stderr
            and "Did you forget to 'git add'?" in command.stderr)


@utils.git_support
def get_new_command(command, settings):
    missing_file = re.findall(
            r"error: pathspec '([^']*)' "
            "did not match any file\(s\) known to git.", command.stderr)[0]

    formatme = shells.and_('git add -- {}', '{}')
    return formatme.format(missing_file, command.script)
