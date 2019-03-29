import pytest
from thefuck.rules.git_branch_0v_to_dash_v import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return ""


def test_match(output):
    assert match(Command('git branch 0v', output))
    assert not match(Command('git branch -v', ''))
    assert not match(Command('ls', output))


def test_get_new_command(output):
    assert get_new_command(Command('git branch 0v', output))\
        == "git branch -D 0v && git branch -v"
