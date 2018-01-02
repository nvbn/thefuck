import pytest
from thefuck.rules.git_push import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output(branch):
    return '''fatal: The current branch {} has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin {}

'''.format(branch, branch)


@pytest.mark.parametrize('command', [
    Command('git push', output('master')),
    Command('git push master', output('master'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('git push master', ''),
    Command('ls', output('master'))])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('git push master', output('master')),
     'git push --set-upstream origin master'),
    (Command('git push master', output('master')),
     'git push --set-upstream origin master'),
    (Command('git push master', output('master')),
     'git push --set-upstream origin master'),
    (Command('git push -u', output('master')),
     'git push --set-upstream origin master'),
    (Command('git push -u origin', output('master')),
     'git push --set-upstream origin master'),
    (Command('git push origin', output('master')),
     'git push --set-upstream origin master'),
    (Command('git push --set-upstream origin', output('master')),
     'git push --set-upstream origin master'),
    (Command('git push --quiet', output('master')),
     'git push --set-upstream origin master --quiet'),
    (Command('git push --quiet origin', output('master')),
     'git push --set-upstream origin master --quiet'),
    (Command('git -c test=test push --quiet origin', output('master')),
     'git -c test=test push --set-upstream origin master --quiet'),
    (Command('git push', output("test's")),
     "git push --set-upstream origin test\\'s")])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
