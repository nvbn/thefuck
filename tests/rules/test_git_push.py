import pytest
from thefuck.main import Command
from thefuck.rules.git_push import match, get_new_command


@pytest.fixture
def stderr():
    return '''fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master

'''


def test_match(stderr):
    assert match(Command('git push master', '', stderr), None)
    assert not match(Command('git push master', '', ''), None)
    assert not match(Command('ls', '', stderr), None)


def test_get_new_command(stderr):
    assert get_new_command(Command('', '', stderr), None)\
        == "git push --set-upstream origin master"
