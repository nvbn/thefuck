# -*- encoding: utf-8 -*-

import sys
from .conf import settings
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
    """Helper for selecting rule from rules list."""

    def __init__(self, commands):
        self._commands_gen = commands
        self._commands = [next(self._commands_gen)]
        self._realised = False
        self._index = 0

    def _realise(self):
        if not self._realised:
            self._commands += list(self._commands_gen)
            self._realised = True

    def next(self):
        self._realise()
        self._index = (self._index + 1) % len(self._commands)

    def previous(self):
        self._realise()
        self._index = (self._index - 1) % len(self._commands)

    @property
    def value(self):
        return self._commands[self._index]


def select_command(corrected_commands):
    """Returns:

     - the first command when confirmation disabled;
     - None when ctrl+c pressed;
     - selected command.

    """
    try:
        selector = CommandSelector(corrected_commands)
    except StopIteration:
        logs.failed('No fucks given')
        return

    if not settings.require_confirmation:
        logs.show_corrected_command(selector.value)
        return selector.value

    logs.confirm_text(selector.value)

    for action in read_actions():
        if action == SELECT:
            sys.stderr.write('\n')
            return selector.value
        elif action == ABORT:
            logs.failed('\nAborted')
            return
        elif action == PREVIOUS:
            selector.previous()
            logs.confirm_text(selector.value)
        elif action == NEXT:
            selector.next()
            logs.confirm_text(selector.value)
