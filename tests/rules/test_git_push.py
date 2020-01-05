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


@pytest.fixture
def output_bitbucket():
    return '''Total 0 (delta 0), reused 0 (delta 0)
remote:
remote: Create pull request for feature/set-upstream:
remote:   https://bitbucket.org/set-upstream
remote:
To git@bitbucket.org:test.git
   e5e7fbb..700d998  feature/set-upstream -> feature/set-upstream
Branch feature/set-upstream set up to track remote branch feature/set-upstream from origin.
'''


@pytest.mark.parametrize('script, branch_name', [
    ('git push', 'master'),
    ('git push origin', 'master')])
def test_match(output, script, branch_name):
    assert match(Command(script, output))


def test_match_bitbucket(output_bitbucket):
    assert not match(Command('git push origin', output_bitbucket))


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
     "git push --set-upstream origin test\\'s"),
    ('git push --force', 'master',
     'git push --set-upstream origin master --force'),
    ('git push --force-with-lease', 'master',
     'git push --set-upstream origin master --force-with-lease')])
def test_get_new_command(output, script, branch_name, new_command):
    assert get_new_command(Command(script, output)) == new_command
