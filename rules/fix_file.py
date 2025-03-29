import re
import os
from thefuck.utils import memoize, default_settings
from thefuck.conf import settings
from thefuck.shells import shell


# order is important: only the first match is considered
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
    '^{file} \\(line {line}\\):',
    # bash, sh, ssh:
    '^{file}: line {line}: ',
    # cargo, clang, gcc, go, pep8, rustc:
    '^{file}:{line}:{col}',
    # ghc, make, ruby, zsh:
    '^{file}:{line}:',
    # perl:
    'at {file} line {line}',
)


# for the sake of readability do not use named groups above
def _make_pattern(pattern):
    pattern = pattern.replace('{file}', '(?P<file>[^:\n]+)') \
                     .replace('{line}', '(?P<line>[0-9]+)') \
                     .replace('{col}', '(?P<col>[0-9]+)')
    return re.compile(pattern, re.MULTILINE)


patterns = [_make_pattern(p).search for p in patterns]


@memoize
def _search(output):
    for pattern in patterns:
        m = pattern(output)
        if m and os.path.isfile(m.group('file')):
            return m


def match(command):
    if 'EDITOR' not in os.environ:
        return False

    return _search(command.output)


@default_settings({'fixlinecmd': u'{editor} {file} +{line}',
                   'fixcolcmd': None})
def get_new_command(command):
    m = _search(command.output)

    # Note: there does not seem to be a standard for columns, so they are just
    # ignored by default
    if settings.fixcolcmd and 'col' in m.groupdict():
        editor_call = settings.fixcolcmd.format(editor=os.environ['EDITOR'],
                                                file=m.group('file'),
                                                line=m.group('line'),
                                                col=m.group('col'))
    else:
        editor_call = settings.fixlinecmd.format(editor=os.environ['EDITOR'],
                                                 file=m.group('file'),
                                                 line=m.group('line'))

    return shell.and_(editor_call, command.script)
