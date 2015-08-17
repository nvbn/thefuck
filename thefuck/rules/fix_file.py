import re
import os
from thefuck.utils import memoize, wrap_settings
from thefuck import shells


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
    pattern = pattern.replace('{file}', '(?P<file>[^:\n]+)')
    pattern = pattern.replace('{line}', '(?P<line>[0-9]+)')
    pattern = pattern.replace('{col}',  '(?P<col>[0-9]+)')
    return re.compile(pattern, re.MULTILINE)
patterns = [_make_pattern(p) for p in patterns]


@memoize
def _search(stderr):
    for pattern in patterns:
        m = re.search(pattern, stderr)
        if m and os.path.isfile(m.group('file')):
            return m


def match(command, settings):
    if 'EDITOR' not in os.environ:
        return False

    return _search(command.stderr) or _search(command.stdout)


@wrap_settings({'fixlinecmd': '{editor} {file} +{line}',
                'fixcolcmd': None})
def get_new_command(command, settings):
    m = _search(command.stderr) or _search(command.stdout)

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

    return shells.and_(editor_call, command.script)
