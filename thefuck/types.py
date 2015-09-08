from collections import namedtuple

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
            return (other.script, other.side_effect) == \
                   (self.script, self.side_effect)
        else:
            return False

    def __hash__(self):
        return (self.script, self.side_effect).__hash__()

    def __repr__(self):
        return 'CorrectedCommand(script={}, side_effect={}, priority={})'.format(
            self.script, self.side_effect, self.priority)


class Settings(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value
