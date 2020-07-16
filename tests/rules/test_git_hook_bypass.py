import pytest
from thefuck.rules.git_hook_bypass import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize(
    "command",
    [
        Command("git am", ""),
        Command("git commit", ""),
        Command("git commit -m 'foo bar'", ""),
        Command("git push", ""),
        Command("git push -u foo bar", ""),
    ],
)
def test_match(command):
    assert match(command)


@pytest.mark.parametrize(
    "command",
    [
        Command("git add foo", ""),
        Command("git status", ""),
        Command("git diff foo bar", ""),
    ],
)
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize(
    "command, new_command",
    [
        (Command("git am", ""), "git am --no-verify"),
        (Command("git commit", ""), "git commit --no-verify"),
        (Command("git commit -m 'foo bar'", ""), "git commit --no-verify -m 'foo bar'"),
        (Command("git push", ""), "git push --no-verify"),
        (Command("git push -p", ""), "git push --no-verify -p"),
    ],
)
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
