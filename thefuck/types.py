from imp import load_source
import os
import sys
from . import logs
from .shells import shell
from .conf import settings
from .const import DEFAULT_PRIORITY, ALL_ENABLED
from .exceptions import EmptyCommand
from .utils import get_alias, format_raw_script
from .output_readers import get_output


class Command(object):
    """Command that should be fixed."""

    def __init__(self, script, output):
        """Initializes command with given values.

        :type script: basestring
        :type output: basestring

        """
        self.script = script
        self.output = output

    @property
    def stdout(self):
        logs.warn('`stdout` is deprecated, please use `output` instead')
        return self.output

    @property
    def stderr(self):
        logs.warn('`stderr` is deprecated, please use `output` instead')
        return self.output

    @property
    def script_parts(self):
        if not hasattr(self, '_script_parts'):
            try:
                self._script_parts = shell.split_command(self.script)
            except Exception:
                logs.debug(u"Can't split command script {} because:\n {}".format(
                    self, sys.exc_info()))
                self._script_parts = []

        return self._script_parts

    def __eq__(self, other):
        if isinstance(other, Command):
            return (self.script, self.output) == (other.script, other.output)
        else:
            return False

    def __repr__(self):
        return u'Command(script={}, output={})'.format(
            self.script, self.output)

    def update(self, **kwargs):
        """Returns new command with replaced fields.

        :rtype: Command

        """
        kwargs.setdefault('script', self.script)
        kwargs.setdefault('output', self.output)
        return Command(**kwargs)

    @classmethod
    def from_raw_script(cls, raw_script):
        """Creates instance of `Command` from a list of script parts.

        :type raw_script: [basestring]
        :rtype: Command
        :raises: EmptyCommand

        """
        script = format_raw_script(raw_script)
        if not script:
            raise EmptyCommand

        expanded = shell.from_shell(script)
        output = get_output(script, expanded)
        return cls(expanded, output)


class Rule(object):
    """Rule for fixing commands."""

    def __init__(self, name, path, match, get_new_command, post_match,
                 enabled_by_default, side_effect,
                 priority, requires_output, is_post_match):
        """Initializes rule with given fields.

        :type name: basestring
        :type match: (Command) -> bool
        :type get_new_command: (Command) -> (basestring | [basestring])
        :type enabled_by_default: boolean
        :type side_effect: (Command, basestring) -> None
        :type priority: int
        :type requires_output: bool

        """
        self.name = name
        self.path = path
        self.match = match
        self.get_new_command = get_new_command
        self.post_match = post_match
        self.enabled_by_default = enabled_by_default
        self.side_effect = side_effect
        self.priority = priority
        self.requires_output = requires_output
        self.is_post_match = is_post_match

    def __eq__(self, other):
        if isinstance(other, Rule):
            return ((self.name, self.path, self.match, self.get_new_command,
                     self.post_match, self.enabled_by_default,
                     self.side_effect, self.priority,
                     self.requires_output, self.is_post_match)
                    == (other.name, other.path, other.match, other.get_new_command,
                        other.post_match, other.enabled_by_default,
                        other.side_effect, other.priority,
                        other.requires_output, other.is_post_match))
        else:
            return False

    def __repr__(self):
        return 'Rule(name={}, path={}, match={}, get_new_command={}, ' \
               'post_match={}, enabled_by_default={}, side_effect={}, ' \
               'priority={}, requires_output={}, is_post_match={})'.format(
                   self.name, self.path, self.match, self.get_new_command,
                   self.post_match, self.enabled_by_default, self.side_effect,
                   self.priority, self.requires_output, self.is_post_match)

    @classmethod
    def from_path(cls, path):
        """Creates rule instance from path.

        :type path: pathlib.Path
        :rtype: Rule

        """
        name = path.name[:-3]
        with logs.debug_time(u'Importing rule: {};'.format(name)):
            rule_module = load_source(name, str(path))
            priority = getattr(rule_module, 'priority', DEFAULT_PRIORITY)
        return cls(name, path.as_posix(), rule_module.match,
                   rule_module.get_new_command,
                   getattr(rule_module, 'post_match', None),
                   getattr(rule_module, 'enabled_by_default', True),
                   getattr(rule_module, 'side_effect', None),
                   settings.priority.get(name, priority),
                   getattr(rule_module, 'requires_output', True),
                   getattr(rule_module, 'is_post_match', False))

    @property
    def is_enabled(self):
        """Returns `True` when rule enabled.

        :rtype: bool

        """
        if self.name in settings.exclude_rules:
            return False
        elif self.name in settings.rules:
            return True
        elif self.enabled_by_default and ALL_ENABLED in settings.rules:
            return True
        else:
            return False

    def is_match(self, command):
        """Returns `True` if rule matches the command.

        :type command: Command
        :rtype: bool

        """
        if command.output is None and self.requires_output:
            return False

        try:
            with logs.debug_time(u'Trying rule: {};'.format(self.name)):
                if self.match(command):
                    return True
        except Exception:
            logs.rule_failed(self, sys.exc_info())

    def get_corrected_commands(self, command):
        """Returns generator with corrected commands.

        :type command: Command
        :rtype: Iterable[CorrectedCommand]

        """
        new_commands = self.get_new_command(command)
        if not isinstance(new_commands, list):
            new_commands = (new_commands,)
        for n, new_command in enumerate(new_commands):
            yield CorrectedCommand(script=new_command,
                                   side_effect=self.side_effect,
                                   priority=(n + 1) * self.priority,
                                   rule=self)


class CorrectedCommand(object):
    """Corrected by rule command."""

    def __init__(self, script, side_effect, priority, rule):
        """Initializes instance with given fields.

        :type script: basestring
        :type side_effect: (Command, basestring) -> None
        :type priority: int

        """
        self.script = script
        self.side_effect = side_effect
        self.priority = priority
        self.rule = rule

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
        return u'CorrectedCommand(script={}, side_effect={}, priority={})'.format(
            self.script, self.side_effect, self.priority)

    def _get_script(self, old_cmd):
        """Returns fixed commands script.

        If `settings.repeat` is `True`, appends command with second attempt
        of running fuck in case fixed command fails again.

        """
        if self.rule and self.rule.is_post_match:
            return u'thefuck --post-match {} {} {}'.format(
                self.rule.path,
                shell.quote(old_cmd.script),
                shell.quote(old_cmd.output))
        elif settings.repeat:
            repeat_fuck = '{} --repeat {}--force-command {}'.format(
                get_alias(),
                '--debug ' if settings.debug else '',
                shell.quote(self.script))
            return shell.or_(self.script, repeat_fuck)
        else:
            return self.script

    def run(self, old_cmd):
        """Runs command from rule for passed command.

        :type old_cmd: Command

        """
        if self.side_effect:
            self.side_effect(old_cmd, self.script)
        if settings.alter_history:
            shell.put_to_history(self.script)
        # This depends on correct setting of PYTHONIOENCODING by the alias:
        logs.debug(u'PYTHONIOENCODING: {}'.format(
            os.environ.get('PYTHONIOENCODING', '!!not-set!!')))

        print(self._get_script(old_cmd))
