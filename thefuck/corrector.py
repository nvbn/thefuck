import sys
from .conf import settings
from .types import Rule
from .system import Path
from . import logs


def get_loaded_rules(rules_paths):
    """Yields all available rules.

    :type rules_paths: [Path]
    :rtype: Iterable[Rule]

    """
    for path in rules_paths:
        if path.name != '__init__.py':
            rule = Rule.from_path(path)
            if rule.is_enabled:
                yield rule


def get_rules_import_paths():
    """Yields all rules import paths.

    :rtype: Iterable[Path]

    """
    # Bundled rules:
    yield Path(__file__).parent.joinpath('rules')
    # Rules defined by user:
    yield settings.user_dir.joinpath('rules')
    # Packages with third-party rules:
    for path in sys.path:
        for contrib_module in Path(path).glob('thefuck_contrib_*'):
            contrib_rules = contrib_module.joinpath('rules')
            if contrib_rules.is_dir():
                yield contrib_rules


def get_rules():
    """Returns all enabled rules.

    :rtype: [Rule]

    """
    paths = [rule_path for path in get_rules_import_paths()
             for rule_path in sorted(path.glob('*.py'))]
    return sorted(get_loaded_rules(paths),
                  key=lambda rule: rule.priority)


def organize_commands(corrected_commands):
    """Yields sorted commands without duplicates.

    :type corrected_commands: Iterable[thefuck.types.CorrectedCommand]
    :rtype: Iterable[thefuck.types.CorrectedCommand]

    """
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
        ', '.join(u'{}'.format(cmd) for cmd in [first_command] + sorted_commands)))

    yield from sorted_commands


def get_corrected_commands(command):
    """Returns generator with sorted and unique corrected commands.

    :type command: thefuck.types.Command
    :rtype: Iterable[thefuck.types.CorrectedCommand]

    """
    corrected_commands = (
        corrected for rule in get_rules()
        if rule.is_match(command)
        for corrected in rule.get_corrected_commands(command))
    return organize_commands(corrected_commands)
