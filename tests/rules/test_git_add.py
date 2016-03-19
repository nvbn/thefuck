import pytest
from thefuck.rules.git_add import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr(target):
    return ("error: pathspec '{}' did not match any "
            'file(s) known to git.'.format(target))


@pytest.mark.parametrize('script, target', [
    ('git submodule update unknown', 'unknown'),
    ('git commit unknown', 'unknown')])
def test_match(stderr, script, target):
    assert match(Command(script=script, stderr=stderr))


@pytest.mark.parametrize('script', [
    'git submodule update known', 'git commit known'])
def test_not_match(script):
    assert not match(Command(script=script, stderr=''))


@pytest.mark.parametrize('script, target, new_command', [
    ('git submodule update unknown', 'unknown',
     'git add -- unknown && git submodule update unknown'),
    ('git commit unknown', 'unknown',
     'git add -- unknown && git commit unknown')])
def test_get_new_command(stderr, script, target, new_command):
    assert get_new_command(Command(script=script, stderr=stderr)) == new_command
