import pytest
from thefuck.rules.remove_shell_prompt_literal import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return "$: command not found"


@pytest.mark.parametrize("script", ["$ cd newdir", " $ cd newdir"])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "command",
    [
        Command("$", "$: command not found"),
        Command(" $", "$: command not found"),
        Command("$?", "127: command not found"),
        Command(" $?", "127: command not found"),
        Command("", ""),
    ],
)
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize(
    "script, new_command",
    [
        ("$ cd newdir", "cd newdir"),
        ("$ python3 -m virtualenv env", "python3 -m virtualenv env"),
    ],
)
def test_get_new_command(script, new_command, output):
    assert get_new_command(Command(script, output)) == new_command
