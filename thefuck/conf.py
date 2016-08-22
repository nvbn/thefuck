from imp import load_source
import os
import sys
from warnings import warn
from six import text_type
from . import const
from .system import Path


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
                settings_file.write(const.SETTINGS_HEADER)
                for setting in const.DEFAULT_SETTINGS.items():
                    settings_file.write(u'# {} = {}\n'.format(*setting))

    def _get_user_dir_path(self):
        """returns Path object representing the user config resource"""
        xdg_config_home = os.getenv("XDG_CONFIG_HOME", "~/.config")
        user_dir_modern = Path(xdg_config_home, 'thefuck').expanduser()
        user_dir_legacy = Path('~', '.thefuck').expanduser()

        # default to standards-based location
        user_dir = user_dir_modern

        # for backward compatibility use legacy '~/.thefuck' if it exists
        if user_dir_legacy.is_dir():
            user_dir = user_dir_legacy
            message = 'config path {} is deprecated. please move to {}'
            warn(message.format(user_dir_legacy, user_dir_modern))

        return user_dir

    def _setup_user_dir(self):
        """Returns user config dir, create it when it doesn't exist."""
        user_dir = self._get_user_dir_path()

        rules_dir = user_dir.joinpath('rules')
        if not rules_dir.is_dir():
            rules_dir.mkdir(parents=True)
        self.user_dir = user_dir

    def _settings_from_file(self):
        """Loads settings from file."""
        settings = load_source(
            'settings', text_type(self.user_dir.joinpath('settings.py')))
        return {key: getattr(settings, key)
                for key in const.DEFAULT_SETTINGS.keys()
                if hasattr(settings, key)}

    def _rules_from_env(self, val):
        """Transforms rules list from env-string to python."""
        val = val.split(':')
        if 'DEFAULT_RULES' in val:
            val = const.DEFAULT_RULES + [rule for rule in val if rule != 'DEFAULT_RULES']
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
        elif attr in ('wait_command', 'history_limit', 'wait_slow_command'):
            return int(val)
        elif attr in ('require_confirmation', 'no_colors', 'debug',
                      'alter_history'):
            return val.lower() == 'true'
        elif attr == 'slow_commands':
            return val.split(':')
        else:
            return val

    def _settings_from_env(self):
        """Loads settings from env."""
        return {attr: self._val_from_env(env, attr)
                for env, attr in const.ENV_TO_ATTR.items()
                if env in os.environ}


settings = Settings(const.DEFAULT_SETTINGS)
