import pytest
from thefuck.rules.git_log import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('script, output', [
    ('git lock', 'git: \'lock\' is not a git command.'),
    ('git lock --help', 'git: \'lock\' is not a git command.')])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', [
    'git branch foo',
    'git checkout feature/test_commit',
    'git push'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, output', [
    ('git lock', 'git log'),
    ('git lock --help', 'git log --help')])
def test_get_new_command(script, output):
    assert get_new_command(Command(script, '')) == output
