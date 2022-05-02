import pytest

from thefuck.rules.ls_r import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize(
    "script, output",
    [("ls -r", "")],
)
def test_not_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [("ls -r", "", "ls -R")],
)
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
