import pytest
from thefuck.rules.git_push import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return '''fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master

'''


def test_match(output):
    assert match(Command('git push', output))
    assert match(Command('git push master', output))
    assert not match(Command('git push master', ''))
    assert not match(Command('ls', output))


def test_get_new_command(output):
    assert get_new_command(Command('git push', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push -u', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push -u origin', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push --set-upstream origin', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push --quiet', output))\
        == "git push --set-upstream origin master --quiet"
