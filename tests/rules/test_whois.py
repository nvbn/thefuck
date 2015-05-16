import pytest
from thefuck.rules.whois import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='whois https://en.wikipedia.org/wiki/Main_Page'),
    Command(script='whois https://en.wikipedia.org/'),
    Command(script='whois en.wikipedia.org')])
def test_match(command):
    assert match(command, None)


@pytest.mark.parametrize('command, new_command', [
    (Command('whois https://en.wikipedia.org/wiki/Main_Page'), 'whois en.wikipedia.org'),
    (Command('whois https://en.wikipedia.org/'), 'whois en.wikipedia.org'),
    (Command('whois en.wikipedia.org'), 'whois wikipedia.org')])
def test_get_new_command(command, new_command):
    assert get_new_command(command, None) == new_command
