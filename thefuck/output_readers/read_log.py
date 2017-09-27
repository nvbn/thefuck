import os
import shlex
try:
    from shutil import get_terminal_size
except ImportError:
    from backports.shutil_get_terminal_size import get_terminal_size
import six
import pyte
from ..exceptions import ScriptNotInLog
from .. import const, logs


def _group_by_calls(log):
    ps1 = os.environ['PS1']
    ps1_newlines = ps1.count('\\n') + ps1.count('\n')
    ps1_counter = 0

    script_line = None
    lines = []
    for line in log:
        try:
            line = line.decode()
        except UnicodeDecodeError:
            continue

        if const.USER_COMMAND_MARK in line or ps1_counter > 0:
            if script_line and ps1_counter == 0:
                yield script_line, lines

            if ps1_newlines > 0:
                if ps1_counter <= 0:
                    ps1_counter = ps1_newlines
                else:
                    ps1_counter -= 1

            script_line = line
            lines = [line]
        elif script_line is not None:
            lines.append(line)

    if script_line:
        yield script_line, lines


def _get_script_group_lines(grouped, script):
    parts = shlex.split(script)

    for script_line, lines in reversed(grouped):
        if all(part in script_line for part in parts):
            return lines

    raise ScriptNotInLog


def _get_output_lines(script, log_file):
    lines = log_file.readlines()[-const.LOG_SIZE:]
    grouped = list(_group_by_calls(lines))
    script_lines = _get_script_group_lines(grouped, script)

    screen = pyte.Screen(get_terminal_size().columns, len(script_lines))
    stream = pyte.Stream(screen)
    stream.feed(''.join(script_lines))
    return screen.display


def _skip_old_lines(log_file):
    size = os.path.getsize(os.environ['THEFUCK_OUTPUT_LOG'])
    if size > const.LOG_SIZE_IN_BYTES:
        log_file.seek(size - const.LOG_SIZE_IN_BYTES)


def get_output(script):
    """Reads script output from log.

    :type script: str
    :rtype: str | None

    """
    if six.PY2:
        logs.warn('Experimental instant mode is Python 3+ only')
        return None

    if 'THEFUCK_OUTPUT_LOG' not in os.environ:
        logs.warn("Output log isn't specified")
        return None

    if const.USER_COMMAND_MARK not in os.environ.get('PS1', ''):
        logs.warn(
            "PS1 doesn't contain user command mark, please ensure "
            "that PS1 is not changed after The Fuck alias initialization")
        return None

    try:
        with logs.debug_time(u'Read output from log'), \
                open(os.environ['THEFUCK_OUTPUT_LOG'], 'rb') as log_file:
            _skip_old_lines(log_file)
            lines = _get_output_lines(script, log_file)
            output = '\n'.join(lines).strip()
            logs.debug(u'Received output: {}'.format(output))
            return output
    except OSError:
        logs.warn("Can't read output log")
        return None
    except ScriptNotInLog:
        logs.warn("Script not found in output log")
        return None
