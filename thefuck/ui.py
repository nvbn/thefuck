import sys
from getch import getch
from . import logs

SELECT = 0
ABORT = 1
PREVIOUS = 2
NEXT = 3


def read_actions():
    """Yields actions for pressed keys."""
    buffer = []
    ch = None
    while True:
        try:
            try:
                ch = getch()
            except OverflowError:  # Ctrl+C, KeyboardInterrupt will be reraised
                pass
        except KeyboardInterrupt:
            yield ABORT

        if ch in ('\n', '\r'):  # Enter
            yield SELECT

        buffer.append(ch)
        buffer = buffer[-3:]

        if buffer == ['\x1b', '[', 'A']:  # ↑
            yield PREVIOUS

        if buffer == ['\x1b', '[', 'B']:  # ↓
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
        logs.failed('No fuck given', settings)
        return

    selector = CommandSelector(corrected_commands)
    if not settings.require_confirmation:
        logs.show_corrected_command(selector.value, settings)
        return selector.value

    selector.on_change(lambda val: logs.confirm_text(val, settings))
    for key in read_actions():
        if key == SELECT:
            sys.stderr.write('\n')
            return selector.value
        elif key == ABORT:
            logs.failed('\nAborted', settings)
            return
        elif key == PREVIOUS:
            selector.previous()
        elif key == NEXT:
            selector.next()
