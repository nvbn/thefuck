import pytest

from thefuck.rules.upper_to_lower_case import match, get_new_command
from thefuck.types import Command



@pytest.mark.parametrize(
    "script, output",
    [
        ("LS", "command not found"),
        ("LS -A", "command not found"),
        ("CD TESTS", "command not found"),
        ("CD tests", "command not found"),
        ("CAT README.MD", "command not found"),
        ("CAT README.md", "command not found"),
        ("MV TESTS TESTING", "command not found"),
        ("GIT ADD .", "command not found"),
        ("GIT add .", "command not found"),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output",
    [
        ("ls", ""),
        ("cd thefuck", ""),
        ("mv tests testing", ""),
        ("git add .", ""),
    ],
)
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        ("LS", "command not found", ["ls"]),
        ("CD TESTS", "command not found", ["cd tests", "cd TESTS"]),
        ("CAT README.MD", "command not found", ["cat readme.md", "cat README.MD"]),
        ("GIT ADD .", "command not found", ["git add ."]),
    ],
)
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
