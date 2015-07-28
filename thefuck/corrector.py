from imp import load_source
from pathlib import Path
from . import conf, types, logs
import sys


def load_rule(rule, settings):
    """Imports rule module and returns it."""
    name = rule.name[:-3]
    rule_module = load_source(name, str(rule))
    priority = getattr(rule_module, 'priority', conf.DEFAULT_PRIORITY)
    return types.Rule(name, rule_module.match,
                      rule_module.get_new_command,
                      getattr(rule_module, 'enabled_by_default', True),
                      getattr(rule_module, 'side_effect', None),
                      settings.priority.get(name, priority),
                      getattr(rule_module, 'requires_output', True))


def get_loaded_rules(rules, settings):
    """Yields all available rules."""
    for rule in rules:
        if rule.name != '__init__.py':
            loaded_rule = load_rule(rule, settings)
            if loaded_rule in settings.rules:
                yield loaded_rule


def get_rules(user_dir, settings):
    """Returns all enabled rules."""
    bundled = Path(__file__).parent \
        .joinpath('rules') \
        .glob('*.py')
    user = user_dir.joinpath('rules').glob('*.py')
    return get_loaded_rules(sorted(bundled) + sorted(user), settings)


def get_matched_rules(command, rules, settings):
    """Returns first matched rule for command."""
    script_only = command.stdout is None and command.stderr is None

    for rule in rules:
        if script_only and rule.requires_output:
            continue

        try:
            with logs.debug_time(u'Trying rule: {};'.format(rule.name),
                                 settings):
                if rule.match(command, settings):
                    yield rule
        except Exception:
            logs.rule_failed(rule, sys.exc_info(), settings)


def make_corrected_commands(command, rules, settings):
    for rule in rules:
        new_commands = rule.get_new_command(command, settings)
        if not isinstance(new_commands, list):
            new_commands = [new_commands]
        for n, new_command in enumerate(new_commands):
            yield types.CorrectedCommand(script=new_command,
                                         side_effect=rule.side_effect,
                                         priority=(n + 1) * rule.priority)


def get_corrected_commands(command, user_dir, settings):
    rules = list(get_rules(user_dir, settings))
    logs.debug(
        u'Loaded rules: {}'.format(', '.join(rule.name for rule in rules)),
        settings)
    matched = list(get_matched_rules(command, rules, settings))
    logs.debug(
        u'Matched rules: {}'.format(', '.join(rule.name for rule in matched)),
        settings)
    corrected_commands = make_corrected_commands(command, matched, settings)
    return sorted(corrected_commands,
                  key=lambda corrected_command: corrected_command.priority)
