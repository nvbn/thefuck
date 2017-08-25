class EmptyCommand(Exception):
    """Raised when empty command passed to `thefuck`."""


class NoRuleMatched(Exception):
    """Raised when no rule matched for some command."""


class ScriptNotInLog(Exception):
    """Script not found in log."""
