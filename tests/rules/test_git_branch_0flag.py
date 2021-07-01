import pytest

from thefuck.rules.git_branch_0flag import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output_branch_exists():
    return "fatal: A branch named 'bar' already exists."


@pytest.mark.parametrize(
    "script",
    [
        "git branch 0a",
        "git branch 0d",
        "git branch 0f",
        "git branch 0r",
        "git branch 0v",
        "git branch 0d foo",
        "git branch 0D foo",
    ],
)
def test_match(script, output_branch_exists):
    assert match(Command(script, output_branch_exists))


@pytest.mark.parametrize(
    "script",
    [
        "git branch -a",
        "git branch -r",
        "git branch -v",
        "git branch -d foo",
        "git branch -D foo",
    ],
)
def test_not_match(script, output_branch_exists):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, new_command",
    [
        ("git branch 0a", "git branch -D 0a && git branch -a"),
        ("git branch 0v", "git branch -D 0v && git branch -v"),
        ("git branch 0d foo", "git branch -D 0d && git branch -d foo"),
        ("git branch 0D foo", "git branch -D 0D && git branch -D foo"),
        ("git branch 0l 'maint-*'", "git branch -D 0l && git branch -l 'maint-*'"),
        ("git branch 0u upstream", "git branch -D 0u && git branch -u upstream"),
    ],
)
def test_get_new_command_branch_exists(script, output_branch_exists, new_command):
    assert get_new_command(Command(script, output_branch_exists)) == new_command


@pytest.fixture
def output_not_valid_object():
    return "fatal: Not a valid object name: 'bar'."


@pytest.mark.parametrize(
    "script, new_command",
    [
        ("git branch 0l 'maint-*'", "git branch -l 'maint-*'"),
        ("git branch 0u upstream", "git branch -u upstream"),
    ],
)
def test_get_new_command_not_valid_object(script, output_not_valid_object, new_command):
    assert get_new_command(Command(script, output_not_valid_object)) == new_command
