from collections import namedtuple


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
