import io
import os
import shlex
import six
from collections import namedtuple
from ..logs import warn
from ..utils import memoize
from ..conf import settings
from ..system import Path


ShellConfiguration = namedtuple('ShellConfiguration', (
    'content', 'path', 'reload', 'can_configure_automatically'))


class Generic(object):
    friendly_name = 'Generic Shell'

    def get_aliases(self):
        return {}

    def _expand_aliases(self, command_script):
        aliases = self.get_aliases()
        binary = command_script.split(' ')[0]
        if binary in aliases:
            return command_script.replace(binary, aliases[binary], 1)
        else:
            return command_script

    def from_shell(self, command_script):
        """Prepares command before running in app."""
        return self._expand_aliases(command_script)

    def to_shell(self, command_script):
        """Prepares command for running in shell."""
        return command_script

    def app_alias(self, alias_name):
        return """alias {0}='eval "$(TF_ALIAS={0} PYTHONIOENCODING=utf-8 """ \
               """thefuck "$(fc -ln -1)")"'""".format(alias_name)

    def instant_mode_alias(self, alias_name):
        warn("Instant mode not supported by your shell")
        return self.app_alias(alias_name)

    def _get_history_file_name(self):
        return ''

    def _get_history_line(self, command_script):
        return ''

    @memoize
    def get_history(self):
        return list(self._get_history_lines())

    def _get_history_lines(self):
        """Returns list of history entries."""
        history_file_name = self._get_history_file_name()
        if os.path.isfile(history_file_name):
            with io.open(history_file_name, 'r',
                         encoding='utf-8', errors='ignore') as history_file:

                lines = history_file.readlines()
                if settings.history_limit:
                    lines = lines[-settings.history_limit:]

                for line in lines:
                    prepared = self._script_from_history(line) \
                        .strip()
                    if prepared:
                        yield prepared

    def and_(self, *commands):
        return u' && '.join(commands)

    def or_(self, *commands):
        return u' || '.join(commands)

    def how_to_configure(self):
        return

    def split_command(self, command):
        """Split the command using shell-like syntax."""
        encoded = self.encode_utf8(command)

        try:
            splitted = [s.replace("??", "\\ ") for s in shlex.split(encoded.replace('\\ ', '??'))]
        except ValueError:
            splitted = encoded.split(' ')

        return self.decode_utf8(splitted)

    def encode_utf8(self, command):
        if six.PY2:
            return command.encode('utf8')
        return command

    def decode_utf8(self, command_parts):
        if six.PY2:
            return [s.decode('utf8') for s in command_parts]
        return command_parts

    def quote(self, s):
        """Return a shell-escaped version of the string s."""

        if six.PY2:
            from pipes import quote
        else:
            from shlex import quote

        return quote(s)

    def _script_from_history(self, line):
        return line

    def put_to_history(self, command):
        """Adds fixed command to shell history.

        In most of shells we change history on shell-level, but not
        all shells support it (Fish).

        """

    def get_builtin_commands(self):
        """Returns shells builtin commands."""
        return ['alias', 'bg', 'bind', 'break', 'builtin', 'case', 'cd',
                'command', 'compgen', 'complete', 'continue', 'declare',
                'dirs', 'disown', 'echo', 'enable', 'eval', 'exec', 'exit',
                'export', 'fc', 'fg', 'getopts', 'hash', 'help', 'history',
                'if', 'jobs', 'kill', 'let', 'local', 'logout', 'popd',
                'printf', 'pushd', 'pwd', 'read', 'readonly', 'return', 'set',
                'shift', 'shopt', 'source', 'suspend', 'test', 'times', 'trap',
                'type', 'typeset', 'ulimit', 'umask', 'unalias', 'unset',
                'until', 'wait', 'while']

    def _get_version(self):
        """Returns the version of the current shell"""
        return ''

    def info(self):
        """Returns the name and version of the current shell"""
        try:
            version = self._get_version()
        except Exception as e:
            warn(u'Could not determine shell version: {}'.format(e))
            version = ''
        return u'{} {}'.format(self.friendly_name, version).rstrip()

    def _create_shell_configuration(self, content, path, reload):
        return ShellConfiguration(
            content=content,
            path=path,
            reload=reload,
            can_configure_automatically=Path(path).expanduser().exists())
