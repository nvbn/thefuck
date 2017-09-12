import os
import shlex
from subprocess import Popen, PIPE, STDOUT
from psutil import Process, TimeoutExpired
from .. import logs
from ..conf import settings


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
            child.kill()
        proc.kill()
        return False


def get_output(script, expanded):
    """Runs the script and obtains stdin/stderr.

    :type script: str
    :type expanded: str
    :rtype: str | None

    """
    env = dict(os.environ)
    env.update(settings.env)

    is_slow = shlex.split(expanded) in settings.slow_commands
    with logs.debug_time(u'Call: {}; with env: {}; is slow: '.format(
            script, env, is_slow)):
        result = Popen(expanded, shell=True, stdin=PIPE,
                       stdout=PIPE, stderr=STDOUT, env=env)
        if _wait_output(result, is_slow):
            output = result.stdout.read().decode('utf-8')
            logs.debug(u'Received output: {}'.format(output))
            return output
        else:
            logs.debug(u'Execution timed out!')
            return None
