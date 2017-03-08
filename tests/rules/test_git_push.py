import pytest
from thefuck.rules.git_push import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return '''fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master

'''


def test_match(stderr):
    assert match(Command('git push', stderr=stderr))
    assert match(Command('git push master', stderr=stderr))
    assert not match(Command('git push master'))
    assert not match(Command('ls', stderr=stderr))


def test_get_new_command(stderr):
    assert get_new_command(Command('git push', stderr=stderr))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push -u', stderr=stderr))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push -u origin', stderr=stderr))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push --set-upstream origin', stderr=stderr))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push --quiet', stderr=stderr))\
        == "git push --set-upstream origin master --quiet"
