import pytest
from thefuck.rules.git_branch_delete import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return '''error: The branch 'branch' is not fully merged.
If you are sure you want to delete it, run 'git branch -D branch'.

'''


def test_match(output):
    assert match(Command('git branch -d branch', output))
    assert not match(Command('git branch -d branch', ''))
    assert not match(Command('ls', output))


def test_get_new_command(output):
    assert get_new_command(Command('git branch -d branch', output))\
        == "git branch -D branch"
