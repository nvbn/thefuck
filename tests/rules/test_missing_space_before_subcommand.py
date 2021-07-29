import pytest
from thefuck.rules.missing_space_before_subcommand import (
    match, get_new_command)
from thefuck.types import Command


@pytest.fixture(autouse=True)
def all_executables(mocker):
    return mocker.patch(
        'thefuck.rules.missing_space_before_subcommand.get_all_executables',
        return_value=['git', 'ls', 'npm', 'w', 'watch'])


@pytest.mark.parametrize('script', [
    'gitbranch', 'ls-la', 'npminstall', 'watchls'])
def test_match(script):
    assert match(Command(script, ''))


@pytest.mark.parametrize('script', ['git branch', 'vimfile'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, result', [
    ('gitbranch', 'git branch'),
    ('ls-la', 'ls -la'),
    ('npminstall webpack', 'npm install webpack'),
    ('watchls', 'watch ls')])
def test_get_new_command(script, result):
    assert get_new_command(Command(script, '')) == result
