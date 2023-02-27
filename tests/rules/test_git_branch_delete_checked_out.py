from mock import patch

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
def test_get_new_command_deletion_flag(script, new_command, output):
    with patch('thefuck.rules.git_branch_delete_checked_out.get_sp_stdout', return_value='master'):
        assert get_new_command(Command(script, output)) == new_command


@pytest.mark.parametrize(
    "script, default_branch",
    [
        ("git branch -d foo", "main"),
        ("git branch -d foo", "bar"),
    ],
)
def test_get_new_command_default_branch(script, default_branch, output):
    with patch('thefuck.rules.git_branch_delete_checked_out.get_sp_stdout', return_value=default_branch):
        assert get_new_command(Command(script, output)) == "git checkout {default_branch} && git branch -D foo".format(default_branch=default_branch)
