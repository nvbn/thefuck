import re
from thefuck.shells import shell
from thefuck.specific.git import git_support


@git_support
def match(command):
    return 'did not match any file(s) known to git.' in command.stderr


@git_support
def get_new_command(command):
    missing_file = re.findall(
        r"error: pathspec '([^']*)' "
        r'did not match any file\(s\) known to git.', command.stderr)[0]

    formatme = shell.and_('git add -- {}', '{}')
    return formatme.format(missing_file, command.script)
