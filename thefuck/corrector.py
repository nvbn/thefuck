import sys
from imp import load_source
from pathlib import Path
from .conf import settings, DEFAULT_PRIORITY
from .types import Rule, CorrectedCommand, SortedCorrectedCommandsSequence
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


def get_loaded_rules(rules):
    """Yields all available rules."""
    for rule in rules:
        if rule.name != '__init__.py':
            loaded_rule = load_rule(rule)
            if loaded_rule in settings.rules and \
                            loaded_rule not in settings.exclude_rules:
                yield loaded_rule


def get_rules(user_dir):
    """Returns all enabled rules."""
    bundled = Path(__file__).parent \
        .joinpath('rules') \
        .glob('*.py')
    user = user_dir.joinpath('rules').glob('*.py')
    return sorted(get_loaded_rules(sorted(bundled) + sorted(user)),
                  key=lambda rule: rule.priority)


def is_rule_match(command, rule):
    """Returns first matched rule for command."""
    script_only = command.stdout is None and command.stderr is None

    if script_only and rule.requires_output:
        return False

    try:
        with logs.debug_time(u'Trying rule: {};'.format(rule.name)):
            if rule.match(command, settings):
                return True
    except Exception:
        logs.rule_failed(rule, sys.exc_info())


def make_corrected_commands(command, rule):
    new_commands = rule.get_new_command(command, settings)
    if not isinstance(new_commands, list):
        new_commands = (new_commands,)
    for n, new_command in enumerate(new_commands):
        yield CorrectedCommand(script=new_command,
                               side_effect=rule.side_effect,
                               priority=(n + 1) * rule.priority)


def get_corrected_commands(command, user_dir):
    corrected_commands = (
        corrected for rule in get_rules(user_dir)
        if is_rule_match(command, rule)
        for corrected in make_corrected_commands(command, rule))
    return SortedCorrectedCommandsSequence(corrected_commands)
