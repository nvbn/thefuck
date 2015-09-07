import pytest
from thefuck.rules.git_pull import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return '''There is no tracking information for the current branch.
Please specify which branch you want to merge with.
See git-pull(1) for details

    git pull <remote> <branch>

If you wish to set tracking information for this branch you can do so with:

    git branch --set-upstream-to=<remote>/<branch> master

'''


def test_match(stderr):
    assert match(Command('git pull', stderr=stderr))
    assert not match(Command('git pull'))
    assert not match(Command('ls', stderr=stderr))


def test_get_new_command(stderr):
    assert get_new_command(Command('git pull', stderr=stderr)) \
           == "git branch --set-upstream-to=origin/master master && git pull"
