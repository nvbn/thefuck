import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from .conf import settings
from .types import Rule
from .system import Path
from . import logs


def get_loaded_rules(rules_paths):
    """Yields all available rules, loading them in parallel.

    :type rules_paths: [Path]
    :rtype: Iterable[Rule]

    """
    paths = [p for p in rules_paths if p.name != '__init__.py']
    if not paths:
        return

    def _load(path):
        rule = Rule.from_path(path)
        if rule and rule.is_enabled:
            return rule
        return None

    with ThreadPoolExecutor(max_workers=min(16, len(paths))) as executor:
        for rule in executor.map(_load, paths):
            if rule is not None:
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


def _filter_paths_for_command(paths, command):
    """Filters rule paths to those relevant for the given command.

    Rules whose filename prefix is a known executable that doesn't match
    the current command are skipped entirely, avoiding both the import
    cost and any subprocess calls in their match() functions.
    """
    from .utils import get_all_executables
    if not command.script_parts:
        return paths
    cmd_name = command.script_parts[0]
    try:
        executables = set(get_all_executables())
    except Exception:
        return paths

    filtered = []
    for path in paths:
        stem = path.stem
        if '_' not in stem:
            # Single-word rule (e.g. sudo.py) — no app prefix, always relevant
            filtered.append(path)
            continue
        prefix = stem.split('_')[0]
        if prefix not in executables:
            # Prefix is descriptive, not an app name (e.g. "missing" in missing_space_before_subcommand)
            filtered.append(path)
        elif prefix == cmd_name:
            # App-specific rule whose prefix matches the current command
            filtered.append(path)
        # else: app-specific rule for a different command, skip to avoid loading it
    return filtered


def get_rules(command=None):
    """Returns all enabled rules, optionally filtered for a specific command.

    :type command: thefuck.types.Command | None
    :rtype: [Rule]

    """
    paths = [rule_path for path in get_rules_import_paths()
             for rule_path in sorted(path.glob('*.py'))]
    if command is not None:
        paths = _filter_paths_for_command(paths, command)
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

    logs.debug(u'Corrected commands: {}'.format(
        ', '.join(u'{}'.format(cmd) for cmd in [first_command] + sorted_commands)))

    for command in sorted_commands:
        yield command


def get_corrected_commands(command):
    """Returns generator with sorted and unique corrected commands.

    Runs rule matching in parallel using a thread pool for lower latency.

    :type command: thefuck.types.Command
    :rtype: Iterable[thefuck.types.CorrectedCommand]

    """
    rules = list(get_rules(command))

    def _check_rule(rule):
        if rule.is_match(command):
            return list(rule.get_corrected_commands(command))
        return []

    corrected = []
    with ThreadPoolExecutor(max_workers=min(16, len(rules) or 1)) as executor:
        for results in executor.map(_check_rule, rules):
            corrected.extend(results)

    return organize_commands(iter(corrected))
