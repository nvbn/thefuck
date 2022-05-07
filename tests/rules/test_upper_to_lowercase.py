import pytest

from thefuck.rules.upper_to_lowercase import match, get_new_command
from thefuck.types import Command



@pytest.mark.parametrize(
    "script, output",
    [
        ("LS", ""),
        ("CD THEFUCK", ""),
        ("CAT README.MD", ""),
        ("MV TESTS TESTING", ""),
        ("GIT ADD .", ""),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output",
    [
        ("ls", ""),
        ("cd thefuck", ""),
        ("cat README.md", ""),
        ("mv tests testing", ""),
        ("git add .", ""),
    ],
)
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        ("LS", "", "ls"),
        ("CD THEFUCK", "", "cd thefuck"),
        ("CAT README.MD", "", "cat readme.md"),
        ("MV TESTS TESTING", "", "mv tests testing"),
        ("GIT ADD .", "", "git add ."),
    ],
)
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command