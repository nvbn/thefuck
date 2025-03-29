import os
import shlex
import six
from subprocess import Popen, PIPE, STDOUT
from psutil import AccessDenied, Process, TimeoutExpired
from .. import logs
from ..conf import settings


def _kill_process(proc):
    """Tries to kill the process otherwise just logs a debug message, the
    process will be killed when thefuck terminates.

    :type proc: Process

    """
    try:
        proc.kill()
    except AccessDenied:
        logs.debug(u'Rerun: process PID {} ({}) could not be terminated'.format(
            proc.pid, proc.exe()))


def _wait_output(popen, is_slow):
    """Returns `True` if we can get output of the command in the
    `settings.wait_command` time.

    Command will be killed if it wasn't finished in the time.

    :type popen: Popen
    :rtype: bool

    """
    proc = Process(popen.pid)
    try:
        proc.wait(settings.wait_slow_command if is_slow
                  else settings.wait_command)
        return True
    except TimeoutExpired:
        for child in proc.children(recursive=True):
            _kill_process(child)
        _kill_process(proc)
        return False


def get_output(script, expanded):
    """Runs the script and obtains stdin/stderr.

    :type script: str
    :type expanded: str
    :rtype: str | None

    """
    env = dict(os.environ)
    env.update(settings.env)

    if six.PY2:
        expanded = expanded.encode('utf-8')

    split_expand = shlex.split(expanded)
    is_slow = split_expand[0] in settings.slow_commands if split_expand else False
    with logs.debug_time(u'Call: {}; with env: {}; is slow: {}'.format(
            script, env, is_slow)):
        result = Popen(expanded, shell=True, stdin=PIPE,
                       stdout=PIPE, stderr=STDOUT, env=env)
        if _wait_output(result, is_slow):
            output = result.stdout.read().decode('utf-8', errors='replace')
            logs.debug(u'Received output: {}'.format(output))
            return output
        else:
            logs.debug(u'Execution timed out!')
            return None
