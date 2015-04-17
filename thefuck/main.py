from collections import namedtuple
from imp import load_source
from pathlib import Path
from os.path import expanduser
from subprocess import Popen, PIPE
import sys


Command = namedtuple('Command', ('script', 'stdout', 'stderr'))
Rule = namedtuple('Rule', ('match', 'get_new_command'))


def setup_user_dir():
    """Returns user config dir, create it when it doesn't exists."""
    user_dir = Path(expanduser('~/.thefuck'))
    if not user_dir.is_dir():
        user_dir.mkdir()
        user_dir.joinpath('rules').mkdir()
        user_dir.joinpath('settings.py').touch()
    return user_dir


def get_settings(user_dir):
    """Returns prepared settings module."""
    settings = load_source('settings',
                           str(user_dir.joinpath('settings.py')))
    if not hasattr(settings, 'rules'):
        settings.rules = None
    return settings


def is_rule_enabled(settings, rule):
    """Returns `True` when rule mentioned in `rules` or `rules`
    isn't defined.

    """
    return settings.rules is None or rule.name[:-3] in settings.rules


def load_rule(rule):
    """Imports rule module and returns it."""
    rule_module = load_source(rule.name[:-3], str(rule))
    return Rule(rule_module.match, rule_module.get_new_command)


def get_rules(user_dir, settings):
    """Returns all enabled rules."""
    bundled = Path(__file__).parent\
                            .joinpath('rules')\
                            .glob('*.py')
    user = user_dir.joinpath('rules').glob('*.py')
    return [load_rule(rule) for rule in list(bundled) + list(user)
            if rule.name != '__init__.py' and is_rule_enabled(settings, rule)]


def get_command(args):
    """Creates command from `args` and executes it."""
    script = ' '.join(args[1:])
    result = Popen(script, shell=True, stdout=PIPE, stderr=PIPE)
    return Command(script, result.stdout.read().decode('utf-8'),
                   result.stderr.read().decode('utf-8'))


def get_matched_rule(command, rules, settings):
    """Returns first matched rule for command."""
    for rule in rules:
        if rule.match(command, settings):
            return rule


def run_rule(rule, command, settings):
    """Runs command from rule for passed command."""
    new_command = rule.get_new_command(command, settings)
    sys.stderr.write(new_command + '\n')
    print(new_command)


def is_second_run(command):
    """It's second run of `fuck`?"""
    return command.script.startswith('fuck')


def main():
    command = get_command(sys.argv)
    if is_second_run(command):
        print("echo Can't fuck twice")
    else:
        user_dir = setup_user_dir()
        settings = get_settings(user_dir)
        rules = get_rules(user_dir, settings)
        matched_rule = get_matched_rule(command, rules, settings)
        if matched_rule:
            run_rule(matched_rule, command, settings)
        else:
            print('echo No fuck given')
