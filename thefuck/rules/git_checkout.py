import re
import subprocess
from thefuck import shells, utils


@utils.git_support
def match(command, settings):
    return ('did not match any file(s) known to git.' in command.stderr
            and "Did you forget to 'git add'?" not in command.stderr)


def get_branches():
    proc = subprocess.Popen(
        ['git', 'branch', '-a', '--no-color', '--no-column'],
        stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
        line = line.decode('utf-8')
        if line.startswith('*'):
            line = line.split(' ')[1]
        if '/' in line:
            line = line.split('/')[-1]
        yield line.strip()


@utils.git_support
def get_new_command(command, settings):
    missing_file = re.findall(
        r"error: pathspec '([^']*)' "
        "did not match any file\(s\) known to git.", command.stderr)[0]
    closest_branch = utils.get_closest(missing_file, get_branches(),
                                       fallback_to_first=False)
    if closest_branch:
        return command.script.replace(missing_file, closest_branch, 1)
    else:
        return shells.and_('git branch {}', '{}').format(
            missing_file, command.script)
