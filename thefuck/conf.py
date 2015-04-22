from copy import copy
from imp import load_source
import os
import sys
from six import text_type
from . import logs


class RulesList(object):
    """Wrapper a top of list for string rules names."""

    def __init__(self, rules):
        self.rules = rules

    def __contains__(self, item):
        return item.name in self.rules

    def __getattr__(self, item):
        return getattr(self.rules, item)

    def __eq__(self, other):
        return self.rules == other


class _DefaultRules(RulesList):
    def __add__(self, items):
        return _DefaultRules(self.rules + items)

    def __contains__(self, item):
        return item.enabled_by_default or \
               super(_DefaultRules, self).__contains__(item)

    def __eq__(self, other):
        if isinstance(other, _DefaultRules):
            return self.rules == other.rules
        else:
            return False


DEFAULT = _DefaultRules([])


class BaseSettings(object):
    def __init__(self, conf):
        self._conf = conf

    def __getattr__(self, item):
        return self._conf.get(item)

    def update(self, **kwargs):
        """Returns new settings with new values from `kwargs`."""
        conf = copy(self._conf)
        conf.update(kwargs)
        return BaseSettings(conf)


class Settings(BaseSettings):
    """Settings loaded from defaults/file/env."""
    defaults = {'rules': DEFAULT,
                'wait_command': 3,
                'require_confirmation': False,
                'no_colors': False}

    env_to_attr = {'THEFUCK_RULES': 'rules',
                   'THEFUCK_WAIT_COMMAND': 'wait_command',
                   'THEFUCK_REQUIRE_CONFIRMATION': 'require_confirmation',
                   'THEFUCK_NO_COLORS': 'no_colors'}

    def __init__(self, user_dir):
        super(Settings, self).__init__(self._load_conf(user_dir))

    def _load_conf(self, user_dir):
        conf = copy(self.defaults)
        try:
            conf.update(self._load_from_file(user_dir))
        except:
            logs.exception("Can't load settings from file",
                           sys.exc_info(),
                           BaseSettings(conf))
        try:
            conf.update(self._load_from_env())
        except:
            logs.exception("Can't load settings from env",
                           sys.exc_info(),
                           BaseSettings(conf))
        if not isinstance(conf['rules'], RulesList):
            conf['rules'] = RulesList(conf['rules'])
        return conf

    def _load_from_file(self, user_dir):
        """Loads settings from file."""
        settings = load_source('settings',
                               text_type(user_dir.joinpath('settings.py')))
        return {key: getattr(settings, key)
                for key in self.defaults.keys()
                if hasattr(settings, key)}

    def _load_from_env(self):
        """Loads settings from env."""
        return {attr: self._val_from_env(env, attr)
                for env, attr in self.env_to_attr.items()
                if env in os.environ}

    def _val_from_env(self, env, attr):
        """Transforms env-strings to python."""
        val = os.environ[env]
        if attr == 'rules':
            val = self._rules_from_env(val)
        elif attr == 'wait_command':
            val = int(val)
        elif attr in ('require_confirmation', 'no_colors'):
            val = val.lower() == 'true'
        return val

    def _rules_from_env(self, val):
        """Transforms rules list from env-string to python."""
        val = val.split(':')
        if 'DEFAULT' in val:
            val = DEFAULT + [rule for rule in val if rule != 'DEFAULT']
        return val
