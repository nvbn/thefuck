import pytest
from thefuck.rules.git_branch_delete_checked_out import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return "error: Cannot delete branch 'foo' checked out at '/bar/foo'"


@pytest.mark.parametrize("script", ["git branch -d foo", "git branch -D foo"])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize("script", ["git branch -d foo", "git branch -D foo"])
def test_not_match(script):
    assert not match(Command(script, "Deleted branch foo (was a1b2c3d)."))


@pytest.mark.parametrize(
    "script, new_command",
    [
        ("git branch -d foo", "git checkout master && git branch -D foo"),
        ("git branch -D foo", "git checkout master && git branch -D foo"),
    ],
)
def test_get_new_command(script, new_command, output):
    assert get_new_command(Command(script, output)) == new_command
