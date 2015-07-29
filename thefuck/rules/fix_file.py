import re
import os
from thefuck.utils import memoize
from thefuck import shells


patterns = (
        # js, node:
        '^    at {file}:{line}:{col}',
        # cargo:
        '^   {file}:{line}:{col}',
        # python, thefuck:
        '^  File "{file}", line {line}',
        # awk:
        '^awk: {file}:{line}:',
        # git
        '^fatal: bad config file line {line} in {file}',
        # llc:
        '^llc: {file}:{line}:{col}:',
        # lua:
        '^lua: {file}:{line}:',
        # fish:
        '^{file} \(line {line}\):',
        # bash, sh, ssh:
        '^{file}: line {line}: ',
        # ghc, make, ruby, zsh:
        '^{file}:{line}:',
        # cargo, clang, gcc, go, rustc:
        '^{file}:{line}:{col}',
        # perl:
        'at {file} line {line}',
    )


# for the sake of readability do not use named groups above
def _make_pattern(pattern):
    pattern = pattern.replace('{file}', '(?P<file>[^:\n]+)')
    pattern = pattern.replace('{line}', '(?P<line>[0-9]+)')
    pattern = pattern.replace('{col}',  '(?P<col>[0-9]+)')
    return re.compile(pattern, re.MULTILINE)
patterns = [_make_pattern(p) for p in patterns]


@memoize
def _search(stderr):
    for pattern in patterns:
        m = re.search(pattern, stderr)
        if m:
            return m


def match(command, settings):
    if 'EDITOR' not in os.environ:
        return False

    m = _search(command.stderr)

    return m and os.path.isfile(m.group('file'))


def get_new_command(command, settings):
    m = _search(command.stderr)

    # Note: there does not seem to be a standard for columns, so they are just
    # ignored for now
    return shells.and_('{} {} +{}'.format(os.environ['EDITOR'], m.group('file'), m.group('line')),
                       command.script)
