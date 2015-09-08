from pathlib import Path
from .conf import settings
from .types import Rule
from . import logs


def get_loaded_rules(rules_paths):
    """Yields all available rules."""
    for path in rules_paths:
        if path.name != '__init__.py':
            rule = Rule.from_path(path)
            if rule.is_enabled:
                yield rule


def get_rules():
    """Returns all enabled rules."""
    bundled = Path(__file__).parent \
        .joinpath('rules') \
        .glob('*.py')
    user = settings.user_dir.joinpath('rules').glob('*.py')
    return sorted(get_loaded_rules(sorted(bundled) + sorted(user)),
                  key=lambda rule: rule.priority)


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
        if rule.is_match(command)
        for corrected in rule.get_corrected_commands(command))
    return organize_commands(corrected_commands)
