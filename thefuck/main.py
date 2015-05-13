from imp import load_source
from pathlib import Path
from os.path import expanduser
from subprocess import Popen, PIPE
import os
import sys
from psutil import Process, TimeoutExpired
import colorama
import six
from . import logs, conf, types, shells


def setup_user_dir():
    """Returns user config dir, create it when it doesn't exist."""
    user_dir = Path(expanduser('~/.thefuck'))
    rules_dir = user_dir.joinpath('rules')
    if not rules_dir.is_dir():
        rules_dir.mkdir(parents=True)
    conf.initialize_settings_file(user_dir)
    return user_dir


def load_rule(rule):
    """Imports rule module and returns it."""
    rule_module = load_source(rule.name[:-3], str(rule))
    return types.Rule(rule.name[:-3], rule_module.match,
                      rule_module.get_new_command,
                      getattr(rule_module, 'enabled_by_default', True),
                      getattr(rule_module, 'side_effect', None),
                      getattr(rule_module, 'priority', conf.DEFAULT_PRIORITY))


def _get_loaded_rules(rules, settings):
    """Yields all available rules."""
    for rule in rules:
        if rule.name != '__init__.py':
            loaded_rule = load_rule(rule)
            if loaded_rule in settings.rules:
                yield loaded_rule


def get_rules(user_dir, settings):
    """Returns all enabled rules."""
    bundled = Path(__file__).parent \
        .joinpath('rules') \
        .glob('*.py')
    user = user_dir.joinpath('rules').glob('*.py')
    rules = _get_loaded_rules(sorted(bundled) + sorted(user), settings)
    return sorted(rules, key=lambda rule: settings.priority.get(
        rule.name, rule.priority))


def wait_output(settings, popen):
    """Returns `True` if we can get output of the command in the
    `wait_command` time.

    Command will be killed if it wasn't finished in the time.

    """
    proc = Process(popen.pid)
    try:
        proc.wait(settings.wait_command)
        return True
    except TimeoutExpired:
        for child in proc.get_children(recursive=True):
            child.kill()
        proc.kill()
        return False


def get_command(settings, args):
    """Creates command from `args` and executes it."""
    if six.PY2:
        script = ' '.join(arg.decode('utf-8') for arg in args[1:])
    else:
        script = ' '.join(args[1:])

    if not script:
        return

    script = shells.from_shell(script)
    result = Popen(script, shell=True, stdout=PIPE, stderr=PIPE,
                   env=dict(os.environ, LANG='C'))
    if wait_output(settings, result):
        return types.Command(script, result.stdout.read().decode('utf-8'),
                             result.stderr.read().decode('utf-8'))


def get_matched_rule(command, rules, settings):
    """Returns first matched rule for command."""
    for rule in rules:
        try:
            if rule.match(command, settings):
                return rule
        except Exception:
            logs.rule_failed(rule, sys.exc_info(), settings)


def confirm(new_command, side_effect, settings):
    """Returns `True` when running of new command confirmed."""
    if not settings.require_confirmation:
        logs.show_command(new_command, side_effect, settings)
        return True

    logs.confirm_command(new_command, side_effect, settings)
    try:
        sys.stdin.read(1)
        return True
    except KeyboardInterrupt:
        logs.failed('Aborted', settings)
        return False


def run_rule(rule, command, settings):
    """Runs command from rule for passed command."""
    new_command = shells.to_shell(rule.get_new_command(command, settings))
    if confirm(new_command, rule.side_effect, settings):
        if rule.side_effect:
            rule.side_effect(command, settings)
        shells.put_to_history(new_command)
        print(new_command)


def main():
    colorama.init()
    user_dir = setup_user_dir()
    settings = conf.get_settings(user_dir)

    command = get_command(settings, sys.argv)
    if command:
        rules = get_rules(user_dir, settings)
        matched_rule = get_matched_rule(command, rules, settings)
        if matched_rule:
            run_rule(matched_rule, command, settings)
            return

    logs.failed('No fuck given', settings)
