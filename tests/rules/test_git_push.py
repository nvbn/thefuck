import pytest
from thefuck.rules.git_push import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output(branch_name):
    if not branch_name:
        return ''
    return '''fatal: The current branch {} has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin {}

'''.format(branch_name, branch_name)


@pytest.mark.parametrize('script, branch_name', [
    ('git push', 'master'),
    ('git push origin', 'master')])
def test_match(output, script, branch_name):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, branch_name', [
    ('git push master', None),
    ('ls', 'master')])
def test_not_match(output, script, branch_name):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, branch_name, new_command', [
    ('git push', 'master',
     'git push --set-upstream origin master'),
    ('git push master', 'master',
     'git push --set-upstream origin master'),
    ('git push -u', 'master',
     'git push --set-upstream origin master'),
    ('git push -u origin', 'master',
     'git push --set-upstream origin master'),
    ('git push origin', 'master',
     'git push --set-upstream origin master'),
    ('git push --set-upstream origin', 'master',
     'git push --set-upstream origin master'),
    ('git push --quiet', 'master',
     'git push --set-upstream origin master --quiet'),
    ('git push --quiet origin', 'master',
     'git push --set-upstream origin master --quiet'),
    ('git -c test=test push --quiet origin', 'master',
     'git -c test=test push --set-upstream origin master --quiet'),
    ('git push', "test's",
     "git push --set-upstream origin test\\'s")])
def test_get_new_command(output, script, branch_name, new_command):
    assert get_new_command(Command(script, output)) == new_command
