import pytest
from thefuck.rules.history import match, get_new_command
from tests.utils import Command


@pytest.fixture
def history(mocker):
    return mocker.patch('thefuck.rules.history.get_history',
                        return_value=['le cat', 'fuck', 'ls cat',
                                      'diff x', 'nocommand x'])


@pytest.fixture
def alias(mocker):
    return mocker.patch('thefuck.rules.history.thefuck_alias',
                        return_value='fuck')


@pytest.fixture
def callables(mocker):
    return mocker.patch('thefuck.rules.history.get_all_executables',
                        return_value=['diff', 'ls'])


@pytest.mark.usefixtures('history', 'callables', 'no_memoize', 'alias')
@pytest.mark.parametrize('script', ['ls cet', 'daff x'])
def test_match(script):
    assert match(Command(script=script))


@pytest.mark.usefixtures('history', 'callables', 'no_memoize', 'alias')
@pytest.mark.parametrize('script', ['apt-get', 'nocommand y'])
def test_not_match(script):
    assert not match(Command(script=script))


@pytest.mark.usefixtures('history', 'callables', 'no_memoize', 'alias')
@pytest.mark.parametrize('script, result', [
    ('ls cet', 'ls cat'),
    ('daff x', 'diff x')])
def test_get_new_command(script, result):
    assert get_new_command(Command(script)) == result
