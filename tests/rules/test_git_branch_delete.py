import pytest
from thefuck.rules.git_branch_delete import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return '''error: The branch 'branch' is not fully merged.
If you are sure you want to delete it, run 'git branch -D branch'.

'''


def test_match(stderr):
    assert match(Command('git branch -d branch', stderr=stderr))
    assert not match(Command('git branch -d branch'))
    assert not match(Command('ls', stderr=stderr))


def test_get_new_command(stderr):
    assert get_new_command(Command('git branch -d branch', stderr=stderr))\
        == "git branch -D branch"
