from collections import namedtuple
from imp import load_source
import sys
from .conf import settings, DEFAULT_PRIORITY, ALL_ENABLED
from .utils import compatibility_call
from . import logs

Command = namedtuple('Command', ('script', 'stdout', 'stderr'))


class Rule(object):
    def __init__(self, name, match, get_new_command,
                 enabled_by_default, side_effect,
                 priority, requires_output):
        self.name = name
        self.match = match
        self.get_new_command = get_new_command
        self.enabled_by_default = enabled_by_default
        self.side_effect = side_effect
        self.priority = priority
        self.requires_output = requires_output

    def __eq__(self, other):
        if isinstance(other, Rule):
            return (self.name, self.match, self.get_new_command,
                    self.enabled_by_default, self.side_effect,
                    self.priority, self.requires_output) \
                   == (other.name, other.match, other.get_new_command,
                       other.enabled_by_default, other.side_effect,
                       other.priority, other.requires_output)
        else:
            return False

    def __repr__(self):
        return 'Rule(name={}, match={}, get_new_command={}, ' \
               'enabled_by_default={}, side_effect={}, ' \
               'priority={}, requires_output)'.format(
                    self.name, self.match, self.get_new_command,
                    self.enabled_by_default, self.side_effect,
                    self.priority, self.requires_output)

    @classmethod
    def from_path(cls, path):
        """Creates rule instance from path."""
        name = path.name[:-3]
        with logs.debug_time(u'Importing rule: {};'.format(name)):
            rule_module = load_source(name, str(path))
            priority = getattr(rule_module, 'priority', DEFAULT_PRIORITY)
        return cls(name, rule_module.match,
                   rule_module.get_new_command,
                   getattr(rule_module, 'enabled_by_default', True),
                   getattr(rule_module, 'side_effect', None),
                   settings.priority.get(name, priority),
                   getattr(rule_module, 'requires_output', True))

    @property
    def is_enabled(self):
        if self.name in settings.exclude_rules:
            return False
        elif self.name in settings.rules:
            return True
        elif self.enabled_by_default and ALL_ENABLED in settings.rules:
            return True
        else:
            return False

    def is_match(self, command):
        """Returns `True` if rule matches the command."""
        script_only = command.stdout is None and command.stderr is None

        if script_only and self.requires_output:
            return False

        try:
            with logs.debug_time(u'Trying rule: {};'.format(self.name)):
                if compatibility_call(self.match, command):
                    return True
        except Exception:
            logs.rule_failed(self, sys.exc_info())

    def get_corrected_commands(self, command):
        new_commands = compatibility_call(self.get_new_command, command)
        if not isinstance(new_commands, list):
            new_commands = (new_commands,)
        for n, new_command in enumerate(new_commands):
            yield CorrectedCommand(script=new_command,
                                   side_effect=self.side_effect,
                                   priority=(n + 1) * self.priority)


class CorrectedCommand(object):
    def __init__(self, script, side_effect, priority):
        self.script = script
        self.side_effect = side_effect
        self.priority = priority

    def __eq__(self, other):
        """Ignores `priority` field."""
        if isinstance(other, CorrectedCommand):
            return (other.script, other.side_effect) == \
                   (self.script, self.side_effect)
        else:
            return False

    def __hash__(self):
        return (self.script, self.side_effect).__hash__()

    def __repr__(self):
        return 'CorrectedCommand(script={}, side_effect={}, priority={})'.format(
            self.script, self.side_effect, self.priority)
