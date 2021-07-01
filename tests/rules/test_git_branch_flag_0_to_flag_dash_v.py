import pytest
from thefuck.rules.git_branch_flag_0_to_flag_dash_v import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return ""


def test_match_git_branch_0v(output):
    assert match(Command('git branch 0v', output))


def test_matches_no__git_branch_0_anything(output):
    assert not match(Command('git branch -v', ''))
    assert not match(Command('ls', output))


def test_get_new_command(output):
    assert get_new_command(Command('git branch 0v', output))\
        == 'git branch -D 0v && git branch -v'
