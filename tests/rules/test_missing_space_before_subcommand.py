import pytest
from thefuck.rules.missing_space_before_subcommand import (
    match, get_new_command)
from tests.utils import Command


@pytest.fixture(autouse=True)
def which(mocker):
    return mocker.patch('thefuck.rules.missing_space_before_subcommand.which',
                        return_value=None)


@pytest.fixture(autouse=True)
def all_executables(mocker):
    return mocker.patch(
        'thefuck.rules.missing_space_before_subcommand.get_all_executables',
        return_value=['git', 'ls', 'npm'])


@pytest.mark.parametrize('script', [
    'gitbranch', 'ls-la', 'npminstall'])
def test_match(script):
    assert match(Command(script))


@pytest.mark.parametrize('script, which_result', [
    ('git branch', '/usr/bin/git'),
    ('vimfile', None)])
def test_not_match(script, which_result, which):
    which.return_value = which_result
    assert not match(Command(script))


@pytest.mark.parametrize('script, result', [
    ('gitbranch', 'git branch'),
    ('ls-la', 'ls -la'),
    ('npminstall webpack', 'npm install webpack')])
def test_get_new_command(script, result):
    assert get_new_command(Command(script)) == result
