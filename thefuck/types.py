from collections import namedtuple


Command = namedtuple('Command', ('script', 'stdout', 'stderr'))

Rule = namedtuple('Rule', ('name', 'match', 'get_new_command',
                           'enabled_by_default'))


class RulesNamesList(list):
    """Wrapper a top of list for string rules names."""

    def __contains__(self, item):
        return super(RulesNamesList, self).__contains__(item.name)


class Settings(dict):

    def __getattr__(self, item):
        return self.get(item)

    def update(self, **kwargs):
        """Returns new settings with new values from `kwargs`."""
        conf = dict(self)
        conf.update(kwargs)
        return Settings(conf)
