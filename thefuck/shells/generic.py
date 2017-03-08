import io
import os
import shlex
import six
from ..utils import memoize
from ..conf import settings


class Generic(object):
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

    def app_alias(self, fuck):
        return "alias {0}='eval $(TF_ALIAS={0} PYTHONIOENCODING=utf-8 " \
               "thefuck $(fc -ln -1))'".format(fuck)

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

    def how_to_configure(self):
        return

    def split_command(self, command):
        """Split the command using shell-like syntax."""
        encoded = self.encode_utf8(command)
        splitted = shlex.split(encoded)
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
