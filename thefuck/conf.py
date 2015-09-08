from imp import load_source
import os
import sys
from pathlib import Path
from six import text_type


ALL_ENABLED = object()
DEFAULT_RULES = [ALL_ENABLED]
DEFAULT_PRIORITY = 1000

DEFAULT_SETTINGS = {'rules': DEFAULT_RULES,
                    'exclude_rules': [],
                    'wait_command': 3,
                    'require_confirmation': True,
                    'no_colors': False,
                    'debug': False,
                    'priority': {},
                    'env': {'LC_ALL': 'C', 'LANG': 'C', 'GIT_TRACE': '1'}}

ENV_TO_ATTR = {'THEFUCK_RULES': 'rules',
               'THEFUCK_EXCLUDE_RULES': 'exclude_rules',
               'THEFUCK_WAIT_COMMAND': 'wait_command',
               'THEFUCK_REQUIRE_CONFIRMATION': 'require_confirmation',
               'THEFUCK_NO_COLORS': 'no_colors',
               'THEFUCK_PRIORITY': 'priority',
               'THEFUCK_DEBUG': 'debug'}

SETTINGS_HEADER = u"""# ~/.thefuck/settings.py: The Fuck settings file
#
# The rules are defined as in the example bellow:
#
# rules = ['cd_parent', 'git_push', 'python_command', 'sudo']
#
# The default values are as follows. Uncomment and change to fit your needs.
# See https://github.com/nvbn/thefuck#settings for more information.
#

"""


class Settings(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

    def init(self):
        """Fills `settings` with values from `settings.py` and env."""
        from .logs import exception

        self._setup_user_dir()
        self._init_settings_file()

        try:
            self.update(self._settings_from_file())
        except Exception:
            exception("Can't load settings from file", sys.exc_info())

        try:
            self.update(self._settings_from_env())
        except Exception:
            exception("Can't load settings from env", sys.exc_info())

    def _init_settings_file(self):
        settings_path = self.user_dir.joinpath('settings.py')
        if not settings_path.is_file():
            with settings_path.open(mode='w') as settings_file:
                settings_file.write(SETTINGS_HEADER)
                for setting in DEFAULT_SETTINGS.items():
                    settings_file.write(u'# {} = {}\n'.format(*setting))

    def _setup_user_dir(self):
        """Returns user config dir, create it when it doesn't exist."""
        user_dir = Path(os.path.expanduser('~/.thefuck'))
        rules_dir = user_dir.joinpath('rules')
        if not rules_dir.is_dir():
            rules_dir.mkdir(parents=True)
        self.user_dir = user_dir

    def _settings_from_file(self):
        """Loads settings from file."""
        settings = load_source(
            'settings', text_type(self.user_dir.joinpath('settings.py')))
        return {key: getattr(settings, key)
                for key in DEFAULT_SETTINGS.keys()
                if hasattr(settings, key)}

    def _rules_from_env(self, val):
        """Transforms rules list from env-string to python."""
        val = val.split(':')
        if 'DEFAULT_RULES' in val:
            val = DEFAULT_RULES + [rule for rule in val if rule != 'DEFAULT_RULES']
        return val

    def _priority_from_env(self, val):
        """Gets priority pairs from env."""
        for part in val.split(':'):
            try:
                rule, priority = part.split('=')
                yield rule, int(priority)
            except ValueError:
                continue

    def _val_from_env(self, env, attr):
        """Transforms env-strings to python."""
        val = os.environ[env]
        if attr in ('rules', 'exclude_rules'):
            return self._rules_from_env(val)
        elif attr == 'priority':
            return dict(self._priority_from_env(val))
        elif attr == 'wait_command':
            return int(val)
        elif attr in ('require_confirmation', 'no_colors', 'debug'):
            return val.lower() == 'true'
        else:
            return val

    def _settings_from_env(self):
        """Loads settings from env."""
        return {attr: self._val_from_env(env, attr)
                for env, attr in ENV_TO_ATTR.items()
                if env in os.environ}


settings = Settings(DEFAULT_SETTINGS)
