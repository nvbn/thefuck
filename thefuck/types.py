from collections import namedtuple
from traceback import format_stack
from .logs import debug

Command = namedtuple('Command', ('script', 'stdout', 'stderr'))

Rule = namedtuple('Rule', ('name', 'match', 'get_new_command',
                           'enabled_by_default', 'side_effect',
                           'priority', 'requires_output'))

class CorrectedCommand(object):
    def __init__(self, script, side_effect, priority):
        self.script = script
        self.side_effect = side_effect
        self.priority = priority

    def __eq__(self, other):
        """Ignores `priority` field."""
        if isinstance(other, CorrectedCommand):
            return (other.script, other.side_effect) ==\
                   (self.script, self.side_effect)
        else:
            return False

    def __hash__(self):
        return (self.script, self.side_effect).__hash__()

    def __repr__(self):
        return 'CorrectedCommand(script={}, side_effect={}, priority={})'.format(
            self.script, self.side_effect, self.priority)


class RulesNamesList(list):
    """Wrapper a top of list for storing rules names."""

    def __contains__(self, item):
        return super(RulesNamesList, self).__contains__(item.name)


class Settings(dict):
    def __getattr__(self, item):
        return self.get(item)

    def update(self, **kwargs):
        """
        Returns new settings with values from `kwargs` for unset settings.
        """
        conf = dict(kwargs)
        conf.update(self)
        return Settings(conf)


class SortedCorrectedCommandsSequence(object):
    """List-like collection/wrapper around generator, that:

    - immediately gives access to the first commands through [];
    - realises generator and sorts commands on first access to other
      commands through [], or when len called.

    """

    def __init__(self, commands, settings):
        self._settings = settings
        self._commands = commands
        self._cached = self._realise_first()
        self._realised = False

    def _realise_first(self):
        try:
            return [next(self._commands)]
        except StopIteration:
            return []

    def _remove_duplicates(self, corrected_commands):
        """Removes low-priority duplicates."""
        commands = {command
                    for command in sorted(corrected_commands,
                                          key=lambda command: -command.priority)
                    if command.script != self._cached[0]}
        return commands

    def _realise(self):
        """Realises generator, removes duplicates and sorts commands."""
        if self._cached:
            commands = self._remove_duplicates(self._commands)
            self._cached = [self._cached[0]] + sorted(
                commands, key=lambda corrected_command: corrected_command.priority)
        self._realised = True
        debug('SortedCommandsSequence was realised with: {}, after: {}'.format(
            self._cached, '\n'.join(format_stack())), self._settings)

    def __getitem__(self, item):
        if item != 0 and not self._realised:
            self._realise()
        return self._cached[item]

    def __bool__(self):
        return bool(self._cached)

    def __len__(self):
        if not self._realised:
            self._realise()
        return len(self._cached)

    def __iter__(self):
        if not self._realised:
            self._realise()
        return iter(self._cached)
