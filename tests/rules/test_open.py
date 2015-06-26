import pytest
from thefuck.rules.open import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='open foo.com'),
    Command(script='open foo.ly'),
    Command(script='open foo.org'),
    Command(script='open foo.net'),
    Command(script='open foo.se'),
    Command(script='open foo.io')])
def test_match(command):
    assert match(command, None)


@pytest.mark.parametrize('command, new_command', [
    (Command('open foo.com'), 'open http://foo.com'),
    (Command('open foo.ly'), 'open http://foo.ly'),
    (Command('open foo.org'), 'open http://foo.org'),
    (Command('open foo.net'), 'open http://foo.net'),
    (Command('open foo.se'), 'open http://foo.se'),
    (Command('open foo.io'), 'open http://foo.io')])
def test_get_new_command(command, new_command):
    assert get_new_command(command, None) == new_command
