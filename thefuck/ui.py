# -*- encoding: utf-8 -*-

import sys
from . import logs

try:
    from msvcrt import getch
except ImportError:
    def getch():
        import tty
        import termios

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x03':  # For compatibility with msvcrt.getch
                raise KeyboardInterrupt
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

SELECT = 0
ABORT = 1
PREVIOUS = 2
NEXT = 3


def read_actions():
    """Yields actions for pressed keys."""
    buffer = []
    while True:
        try:
            ch = getch()
        except KeyboardInterrupt:  # Ctrl+C
            yield ABORT

        if ch in ('\n', '\r'):  # Enter
            yield SELECT

        buffer.append(ch)
        buffer = buffer[-3:]

        if buffer == ['\x1b', '[', 'A']:  # ↑
            yield PREVIOUS
        elif buffer == ['\x1b', '[', 'B']:  # ↓
            yield NEXT


class CommandSelector(object):
    def __init__(self, commands):
        self._commands = commands
        self._index = 0
        self._on_change = lambda x: x

    def next(self):
        self._index = (self._index + 1) % len(self._commands)
        self._on_change(self.value)

    def previous(self):
        self._index = (self._index - 1) % len(self._commands)
        self._on_change(self.value)

    @property
    def value(self):
        return self._commands[self._index]

    def on_change(self, fn):
        self._on_change = fn
        fn(self.value)


def select_command(corrected_commands, settings):
    """Returns:

     - the first command when confirmation disabled;
     - None when ctrl+c pressed;
     - selected command.

    """
    if not corrected_commands:
        logs.failed('No fucks given', settings)
        return

    selector = CommandSelector(corrected_commands)
    if not settings.require_confirmation:
        logs.show_corrected_command(selector.value, settings)
        return selector.value

    selector.on_change(
        lambda val: logs.confirm_text(val, corrected_commands.is_multiple,
                                      settings))
    for action in read_actions():
        if action == SELECT:
            sys.stderr.write('\n')
            return selector.value
        elif action == ABORT:
            logs.failed('\nAborted', settings)
            return
        elif action == PREVIOUS:
            selector.previous()
        elif action == NEXT:
            selector.next()
