import pytest
from thefuck.rules.git_rm_local_modifications import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr(target):
    return ('error: the following file has local modifications:\n    {}\n(use '
            '--cached to keep the file, or -f to force removal)').format(target)


@pytest.mark.parametrize('script, target', [
    ('git rm foo', 'foo'),
    ('git rm foo bar', 'bar')])
def test_match(stderr, script, target):
    assert match(Command(script=script, stderr=stderr))


@pytest.mark.parametrize('script', ['git rm foo', 'git rm foo bar', 'git rm'])
def test_not_match(script):
    assert not match(Command(script=script, stderr=''))


@pytest.mark.parametrize('script, target, new_command', [
    ('git rm foo', 'foo', ['git rm --cached foo', 'git rm -f foo']),
    ('git rm foo bar', 'bar', ['git rm --cached foo bar', 'git rm -f foo bar'])])
def test_get_new_command(stderr, script, target, new_command):
    assert get_new_command(Command(script=script, stderr=stderr)) == new_command
