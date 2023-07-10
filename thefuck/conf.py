import os
import sys
from warnings import warn
from six import text_type
from . import const
from .system import Path

try:
    import importlib.util

    def load_source(name, pathname, _file=None):
        module_spec = importlib.util.spec_from_file_location(name, pathname)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module
except ImportError:
    from imp import load_source


class Settings(dict):
    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

    def init(self, args=None):
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

        self.update(self._settings_from_args(args))

    def _init_settings_file(self):
        settings_path = self.user_dir.joinpath('settings.py')
        if not settings_path.is_file():
            with settings_path.open(mode='w') as settings_file:
                settings_file.write(const.SETTINGS_HEADER)
                for setting in const.DEFAULT_SETTINGS.items():
                    settings_file.write(u'# {} = {}\n'.format(*setting))

    def _get_user_dir_path(self):
        """Returns Path object representing the user config resource"""
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME', '~/.config')
        user_dir = Path(xdg_config_home, 'thefuck').expanduser()
        legacy_user_dir = Path('~', '.thefuck').expanduser()

        # For backward compatibility use legacy '~/.thefuck' if it exists:
        if legacy_user_dir.is_dir():
            warn(u'Config path {} is deprecated. Please move to {}'.format(
                legacy_user_dir, user_dir))
            return legacy_user_dir
        else:
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
        elif attr in ('wait_command', 'history_limit', 'wait_slow_command',
                      'num_close_matches'):
            return int(val)
        elif attr in ('require_confirmation', 'no_colors', 'debug',
                      'alter_history', 'instant_mode'):
            return val.lower() == 'true'
        elif attr in ('slow_commands', 'excluded_search_path_prefixes'):
            return val.split(':')
        else:
            return val

    def _settings_from_env(self):
        """Loads settings from env."""
        return {attr: self._val_from_env(env, attr)
                for env, attr in const.ENV_TO_ATTR.items()
                if env in os.environ}

    def _settings_from_args(self, args):
        """Loads settings from args."""
        if not args:
            return {}

        from_args = {}
        if args.yes:
            from_args['require_confirmation'] = not args.yes
        if args.debug:
            from_args['debug'] = args.debug
        if args.repeat:
            from_args['repeat'] = args.repeat
        return from_args


settings = Settings(const.DEFAULT_SETTINGS)
