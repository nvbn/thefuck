import pytest
from thefuck.rules.history import match, get_new_command
from tests.utils import Command


@pytest.fixture(autouse=True)
def history_without_current(mocker):
    return mocker.patch(
        'thefuck.rules.history.get_valid_history_without_current',
        return_value=['ls cat', 'diff x'])


@pytest.mark.parametrize('script', ['ls cet', 'daff x'])
def test_match(script):
    assert match(Command(script=script))


@pytest.mark.parametrize('script', ['apt-get', 'nocommand y'])
def test_not_match(script):
    assert not match(Command(script=script))


@pytest.mark.parametrize('script, result', [
    ('ls cet', 'ls cat'),
    ('daff x', 'diff x')])
def test_get_new_command(script, result):
    assert get_new_command(Command(script)) == result
