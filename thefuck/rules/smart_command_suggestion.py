"""Suggest likely commands when the shell cannot find a command.

This rule complements ``no_command``.  ``no_command`` uses a relatively
strict fuzzy-match threshold; this rule provides a second, more permissive
fallback so that less obvious typos can still produce useful suggestions.
"""

import os
import re

from thefuck.utils import (
    get_all_executables,
    get_close_matches,
    get_valid_history_without_current,
    replace_argument,
    which,
)


def _is_command_not_found(command):
    """Return True when the shell reports that the command was not found."""
    if not command.script_parts:
        return False

    if which(command.script_parts[0]) is not None:
        return False

    output = command.output or ''

    return any(message in output.lower() for message in (
        'not found',
        'command not found',
        'is not recognized as',
    ))


def _normalize_candidate(candidate):
    """Normalize an executable name for fuzzy matching."""
    candidate = os.path.basename(candidate)

    if os.name == 'nt':
        candidate = re.sub(
            r'\.(exe|cmd|bat|com)$',
            '',
            candidate,
            flags=re.IGNORECASE,
        )

        if candidate.lower().endswith('.dll'):
            return ''

    return candidate


def _candidates(command):
    """Return command candidates from history and PATH."""
    typed = command.script_parts[0].lower()

    history = []
    for script in get_valid_history_without_current(command):
        parts = script.split()
        if parts:
            history.append(parts[0])

    candidates = []

    for candidate in history + list(get_all_executables()):
        candidate = _normalize_candidate(candidate)

        if not candidate:
            continue

        # Never use the failed command itself as a suggestion.
        if candidate.lower() == typed:
            continue

        if candidate not in candidates:
            candidates.append(candidate)

    return candidates


def match(command):
    """Determine whether this rule can suggest a replacement."""
    if not command.script_parts:
        return False

    if not _is_command_not_found(command):
        return False

    typed = command.script_parts[0]

    return bool(
        get_close_matches(
            typed,
            _candidates(command),
            cutoff=0.35,
        )
    )


def get_new_command(command):
    """Return corrected versions of the failed command."""
    typed = command.script_parts[0]

    matches = get_close_matches(
        typed,
        _candidates(command),
        n=5,
        cutoff=0.35,
    )

    return [
        command.script.replace(typed, match, 1)
        for match in matches
    ]

priority = 3500