# -*- encoding: utf-8 -*-

import sys
from .conf import settings
from .exceptions import NoRuleMatched
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

        if buffer == ['\x1b', '[', 'A'] or ch == 'k':  # ↑
            yield PREVIOUS
        elif buffer == ['\x1b', '[', 'B'] or ch == 'j':  # ↓
            yield NEXT


class CommandSelector(object):
    """Helper for selecting rule from rules list."""

    def __init__(self, commands):
        """:type commands: Iterable[thefuck.types.CorrectedCommand]"""
        self._commands_gen = commands
        try:
            self._commands = [next(self._commands_gen)]
        except StopIteration:
            raise NoRuleMatched
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
        """:rtype hefuck.types.CorrectedCommand"""
        return self._commands[self._index]


def select_command(corrected_commands):
    """Returns:

     - the first command when confirmation disabled;
     - None when ctrl+c pressed;
     - selected command.

    :type corrected_commands: Iterable[thefuck.types.CorrectedCommand]
    :rtype: thefuck.types.CorrectedCommand | None

    """
    try:
        selector = CommandSelector(corrected_commands)
    except NoRuleMatched:
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
