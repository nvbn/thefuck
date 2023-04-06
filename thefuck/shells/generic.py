import io
import os
import shlex
import six
from collections import namedtuple
from ..logs import warn, debug
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
        lines = []

        # If atuin_path is provided, then that means
        # we should use it over the normal shell history.
        #
        # TODO: Have some way to fallback to normal shell
        # history if an exception occurs when dealing with the
        # atuin database
        if settings.atuin_path != '':
            # Import sqlite3 and connect to the database
            import sqlite3

            # TODO: Make this connect as read-only
            conn = sqlite3.connect(settings.atuin_path)
            cur = conn.cursor()

            # We use a try except loop here to absolutely make
            # sure the connection is closed, even if there's an
            # exception.
            try:
                # Select the command column, fetch all the
                # rows, and get the command in each row
                cur.execute("SELECT command FROM history")
                rows = cur.fetchall()
                lines = [row[0] for row in rows]
                if settings.history_limit:
                    lines = lines[-settings.history_limit:]

                # Never a bad idea to have a debug statement
                # when dealing with sqlite.
                debug(str(lines))

            # If any exception occurs, we should
            # print the error
            except Exception as e:
                print(e)

            # Close the connection. Finally is
            # always executed regardless if there's
            # an exception or not
            finally:
                conn.close()
        else:
            history_file_name = self._get_history_file_name()
            if os.path.isfile(history_file_name):
                with io.open(history_file_name, 'r',
                             encoding='utf-8',
                             errors='ignore') as history_file:

                    lines = history_file.readlines()
                    if settings.history_limit:
                        lines = lines[-settings.history_limit:]

        # It doesn't matter if we use atuin or just
        # the normal shell history, we'll still have
        # lines to work with
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
