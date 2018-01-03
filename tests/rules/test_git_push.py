import pytest
from thefuck.rules.git_push import match, get_new_command
from thefuck.types import Command


@pytest.fixture(scope='function')
def output(request):
    if not request.param:
        return ''
    return '''fatal: The current branch {} has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin {}

'''.format(request.param, request.param)


@pytest.mark.parametrize('script, output', [
    ('git push', 'master'),
    ('git push origin', 'master')], indirect=['output'])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('git push master', None),
    ('ls', 'master')], indirect=['output'])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, output, new_command', [
    ('git push master', 'master',
     'git push --set-upstream origin master'),
    ('git push master', 'master',
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
     "git push --set-upstream origin test\\'s")], indirect=['output'])
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
