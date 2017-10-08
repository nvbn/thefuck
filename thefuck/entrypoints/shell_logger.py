import array
import fcntl
from functools import partial
import os
import pty
import signal
import sys
import termios
import tty
from ..logs import warn


def _read(f, fd):
    data = os.read(fd, 1024)
    f.write(data)
    f.flush()
    return data


def _set_pty_size(master_fd):
    buf = array.array('h', [0, 0, 0, 0])
    fcntl.ioctl(pty.STDOUT_FILENO, termios.TIOCGWINSZ, buf, True)
    fcntl.ioctl(master_fd, termios.TIOCSWINSZ, buf)


def _spawn(shell, master_read):
    """Create a spawned process.

    Modified version of pty.spawn with terminal size support.

    """
    pid, master_fd = pty.fork()

    if pid == pty.CHILD:
        os.execlp(shell, shell)

    try:
        mode = tty.tcgetattr(pty.STDIN_FILENO)
        tty.setraw(pty.STDIN_FILENO)
        restore = True
    except tty.error:    # This is the same as termios.error
        restore = False

    _set_pty_size(master_fd)
    signal.signal(signal.SIGWINCH, lambda *_: _set_pty_size(master_fd))

    try:
        pty._copy(master_fd, master_read, pty._read)
    except OSError:
        if restore:
            tty.tcsetattr(pty.STDIN_FILENO, tty.TCSAFLUSH, mode)

    os.close(master_fd)
    return os.waitpid(pid, 0)[1]


def shell_logger(output):
    """Logs shell output to the `output`.

    Works like unix script command with `-f` flag.

    """
    if not os.environ.get('SHELL'):
        warn("Shell logger doesn't support your platform.")
        sys.exit(1)

    with open(output, 'wb') as f:
        return_code = _spawn(os.environ['SHELL'], partial(_read, f))

    sys.exit(return_code)
