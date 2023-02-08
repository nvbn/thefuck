import re
from subprocess import PIPE, Popen

from thefuck.utils import eager, memoize, which

npm_available = bool(which('npm'))


@memoize
@eager
def get_scripts():
    """Get custom npm scripts."""
    proc = Popen(['npm', 'run-script'], stdout=PIPE)
    should_yeild = False
    for line in proc.stdout.readlines():
        line = line.decode()
        if 'available via `npm run-script`:' in line:
            should_yeild = True
            continue

        if should_yeild and re.match(r'^  [^ ]+', line):
            yield line.strip().split(' ')[0]
