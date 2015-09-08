import sys
from imp import load_source
from pathlib import Path
from .conf import settings, DEFAULT_PRIORITY, ALL_ENABLED
from .types import Rule, CorrectedCommand
from .utils import compatibility_call
from . import logs


def load_rule(rule):
    """Imports rule module and returns it."""
    name = rule.name[:-3]
    with logs.debug_time(u'Importing rule: {};'.format(name)):
        rule_module = load_source(name, str(rule))
        priority = getattr(rule_module, 'priority', DEFAULT_PRIORITY)
    return Rule(name, rule_module.match,
                rule_module.get_new_command,
                getattr(rule_module, 'enabled_by_default', True),
                getattr(rule_module, 'side_effect', None),
                settings.priority.get(name, priority),
                getattr(rule_module, 'requires_output', True))


def is_rule_enabled(rule):
    """Returns `True` when rule enabled."""
    if rule.name in settings.exclude_rules:
        return False
    elif rule.name in settings.rules:
        return True
    elif rule.enabled_by_default and ALL_ENABLED in settings.rules:
        return True
    else:
        return False


def get_loaded_rules(rules):
    """Yields all available rules."""
    for rule in rules:
        if rule.name != '__init__.py':
            loaded_rule = load_rule(rule)
            if is_rule_enabled(loaded_rule):
                yield loaded_rule


def get_rules():
    """Returns all enabled rules."""
    bundled = Path(__file__).parent \
        .joinpath('rules') \
        .glob('*.py')
    user = settings.user_dir.joinpath('rules').glob('*.py')
    return sorted(get_loaded_rules(sorted(bundled) + sorted(user)),
                  key=lambda rule: rule.priority)


def is_rule_match(command, rule):
    """Returns first matched rule for command."""
    script_only = command.stdout is None and command.stderr is None

    if script_only and rule.requires_output:
        return False

    try:
        with logs.debug_time(u'Trying rule: {};'.format(rule.name)):
            if compatibility_call(rule.match, command):
                return True
    except Exception:
        logs.rule_failed(rule, sys.exc_info())


def make_corrected_commands(command, rule):
    new_commands = compatibility_call(rule.get_new_command, command)
    if not isinstance(new_commands, list):
        new_commands = (new_commands,)
    for n, new_command in enumerate(new_commands):
        yield CorrectedCommand(script=new_command,
                               side_effect=rule.side_effect,
                               priority=(n + 1) * rule.priority)

def organize_commands(corrected_commands):
    """Yields sorted commands without duplicates."""
    try:
        first_command = next(corrected_commands)
        yield first_command
    except StopIteration:
        return

    without_duplicates = {
        command for command in sorted(
            corrected_commands, key=lambda command: command.priority)
        if command != first_command}

    sorted_commands = sorted(
        without_duplicates,
        key=lambda corrected_command: corrected_command.priority)

    logs.debug('Corrected commands: '.format(
        ', '.join(str(cmd) for cmd in [first_command] + sorted_commands)))

    for command in sorted_commands:
        yield command


def get_corrected_commands(command):
    corrected_commands = (
        corrected for rule in get_rules()
        if is_rule_match(command, rule)
        for corrected in make_corrected_commands(command, rule))
    return organize_commands(corrected_commands)
