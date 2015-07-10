import pytest
from thefuck.rules.no_command import match, get_new_command, get_all_callables
from tests.utils import Command


@pytest.fixture(autouse=True)
def _safe(mocker):
    mocker.patch('thefuck.rules.no_command._safe', return_value=[])


@pytest.fixture(autouse=True)
def get_aliases(mocker):
    mocker.patch('thefuck.rules.no_command.get_aliases',
                 return_value=['vim', 'apt-get', 'fsck', 'fuck'])


@pytest.mark.usefixtures('no_memoize')
def test_get_all_callables(*args):
    all_callables = get_all_callables()
    assert 'vim' in all_callables
    assert 'fsck' in all_callables
    assert 'fuck' not in all_callables


@pytest.mark.usefixtures('no_memoize')
def test_match(*args):
    assert match(Command(stderr='vom: not found', script='vom file.py'), None)
    assert match(Command(stderr='fucck: not found', script='fucck'), None)
    assert not match(Command(stderr='qweqwe: not found', script='qweqwe'), None)
    assert not match(Command(stderr='some text', script='vom file.py'), None)


@pytest.mark.usefixtures('no_memoize')
def test_get_new_command(*args):
    assert get_new_command(
        Command(stderr='vom: not found',
                script='vom file.py'),
        None) == 'vim file.py'
    assert get_new_command(
        Command(stderr='fucck: not found',
                script='fucck'),
        Command) == 'fsck'
