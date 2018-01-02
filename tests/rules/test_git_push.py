import pytest
from thefuck.rules.git_push import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return '''fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master

'''


@pytest.fixture
def output_bitbucket():
    return '''Total 0 (delta 0), reused 0 (delta 0)
remote:
remote: Create pull request for feature/[...]:
remote:   https://bitbucket.org/[...]
remote:
To git@bitbucket.org:[...].git
   e5e7fbb..700d998  feature/[...] -> feature/[...]
Branch feature/[...] set up to track remote branch feature/[...] from origin.
'''


def test_match(output):
    assert match(Command('git push', output))
    assert match(Command('git push master', output))
    assert not match(Command('git push master', ''))
    assert not match(Command('ls', output))


def test_match_bitbucket(output_bitbucket):
    assert not match(Command('git push origin', output_bitbucket))


def test_get_new_command(output):
    assert get_new_command(Command('git push', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push master', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push -u', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push -u origin', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push origin', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push --set-upstream origin', output))\
        == "git push --set-upstream origin master"
    assert get_new_command(Command('git push --quiet', output))\
        == "git push --set-upstream origin master --quiet"
    assert get_new_command(Command('git push --quiet origin', output))\
        == "git push --set-upstream origin master --quiet"
    assert get_new_command(Command('git -c test=test push --quiet origin', output))\
        == "git -c test=test push --set-upstream origin master --quiet"
