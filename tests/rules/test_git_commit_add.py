import pytest
from thefuck.rules.git_commit_add import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('script, output', [
    ('git commit -m "test"', 'no changes added to commit'),
    ('git commit', 'no changes added to commit')])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('git commit -m "test"', ' 1 file changed, 15 insertions(+), 14 deletions(-)')])
def test_not_match(output, script):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script', [
    'git branch foo',
    'git checkout feature/test_commit',
    'git push'])
def test_not_match_either(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script', [
    ('git commit')])
def test_get_new_command_one(script):
    assert get_new_command(Command(script, '')) == 'git commit -a'


@pytest.mark.parametrize('script', [
    ('git commit -m "test commit"')])
def test_get_new_command_two(script):
    assert get_new_command(Command(script, '')) == 'git commit -a -m "test commit"'
