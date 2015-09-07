import pytest
from thefuck.rules.no_command import match, get_new_command
from tests.utils import Command


@pytest.fixture(autouse=True)
def get_all_executables(mocker):
    mocker.patch('thefuck.rules.no_command.get_all_executables',
                 return_value=['vim', 'apt-get', 'fsck'])


@pytest.mark.usefixtures('no_memoize')
def test_match():
    assert match(Command(stderr='vom: not found', script='vom file.py'))
    assert match(Command(stderr='fucck: not found', script='fucck'))
    assert not match(Command(stderr='qweqwe: not found', script='qweqwe'))
    assert not match(Command(stderr='some text', script='vom file.py'))


@pytest.mark.usefixtures('no_memoize')
def test_get_new_command():
    assert get_new_command(
        Command(stderr='vom: not found',
                script='vom file.py')) == ['vim file.py']
    assert get_new_command(
        Command(stderr='fucck: not found',
                script='fucck')) == ['fsck']
