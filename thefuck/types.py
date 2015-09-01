from collections import namedtuple
from traceback import format_stack
from .logs import debug

Command = namedtuple('Command', ('script', 'stdout', 'stderr'))

CorrectedCommand = namedtuple('CorrectedCommand', ('script', 'side_effect', 'priority'))

Rule = namedtuple('Rule', ('name', 'match', 'get_new_command',
                           'enabled_by_default', 'side_effect',
                           'priority', 'requires_output'))


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
        self._cached = self._get_first_two_unique()
        self._realised = False

    def _get_first_two_unique(self):
        """Returns first two unique commands."""
        try:
            first = next(self._commands)
        except StopIteration:
            return []

        for command in self._commands:
            if command.script != first.script or \
                            command.side_effect != first.side_effect:
                return [first, command]
        return [first]

    def _remove_duplicates(self, corrected_commands):
        """Removes low-priority duplicates."""
        commands = {(command.script, command.side_effect): command
                    for command in sorted(corrected_commands,
                                          key=lambda command: -command.priority)
                    if command.script != self._cached[0].script
                    or command.side_effect != self._cached[0].side_effect}
        return commands.values()

    def _realise(self):
        """Realises generator, removes duplicates and sorts commands."""
        commands = self._cached[1:] + list(self._commands)
        commands = self._remove_duplicates(commands)
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

    @property
    def is_multiple(self):
        return len(self._cached) > 1
