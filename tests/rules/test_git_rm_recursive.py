import pytest
from thefuck.rules.git_rm_recursive import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr(target):
    return "fatal: not removing '{}' recursively without -r".format(target)


@pytest.mark.parametrize('script, target', [
    ('git rm foo', 'foo'),
    ('git rm foo bar', 'foo bar')])
def test_match(stderr, script, target):
    assert match(Command(script=script, stderr=stderr))


@pytest.mark.parametrize('script', ['git rm foo', 'git rm foo bar'])
def test_not_match(script):
    assert not match(Command(script=script, stderr=''))


@pytest.mark.parametrize('script, target, new_command', [
    ('git rm foo', 'foo', 'git rm -r foo'),
    ('git rm foo bar', 'foo bar', 'git rm -r foo bar')])
def test_get_new_command(stderr, script, target, new_command):
    assert get_new_command(Command(script=script, stderr=stderr)) == new_command
