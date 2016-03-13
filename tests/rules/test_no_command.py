import pytest
from thefuck.rules.no_command import match, get_new_command
from tests.utils import Command


@pytest.fixture(autouse=True)
def get_all_executables(mocker):
    mocker.patch('thefuck.rules.no_command.get_all_executables',
                 return_value=['vim', 'fsck', 'git', 'go'])


@pytest.fixture(autouse=True)
def history_without_current(mocker):
    return mocker.patch(
        'thefuck.rules.no_command.get_valid_history_without_current',
        return_value=['git commit'])


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('script, stderr', [
    ('vom file.py', 'vom: not found'),
    ('fucck', 'fucck: not found'),
    ('got commit', 'got: command not found')])
def test_match(script, stderr):
    assert match(Command(script, stderr=stderr))


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('script, stderr', [
    ('qweqwe', 'qweqwe: not found'),
    ('vom file.py', 'some text')])
def test_not_match(script, stderr):
    assert not match(Command(script, stderr=stderr))


@pytest.mark.usefixtures('no_memoize')
@pytest.mark.parametrize('script, result', [
    ('vom file.py', ['vim file.py']),
    ('fucck', ['fsck']),
    ('got commit', ['git commit', 'go commit'])])
def test_get_new_command(script, result):
    assert get_new_command(Command(script)) == result
