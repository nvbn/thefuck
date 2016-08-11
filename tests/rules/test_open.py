import pytest
from thefuck.rules.open import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr(script):
    return 'The file {} does not exist.\n'.format(script.split(' ', 1)[1])


@pytest.mark.parametrize('script', [
    'open foo.com',
    'open foo.ly',
    'open foo.org',
    'open foo.net',
    'open foo.se',
    'open foo.io',
    'xdg-open foo.com',
    'gnome-open foo.com',
    'kde-open foo.com'])
def test_match(script, stderr):
    assert match(Command(script, stderr=stderr))


@pytest.mark.parametrize('script, new_command', [
    ('open foo.com', 'open http://foo.com'),
    ('open foo.ly', 'open http://foo.ly'),
    ('open foo.org', 'open http://foo.org'),
    ('open foo.net', 'open http://foo.net'),
    ('open foo.se', 'open http://foo.se'),
    ('open foo.io', 'open http://foo.io'),
    ('xdg-open foo.io', 'xdg-open http://foo.io'),
    ('gnome-open foo.io', 'gnome-open http://foo.io'),
    ('kde-open foo.io', 'kde-open http://foo.io')])
def test_get_new_command(script, new_command, stderr):
    assert get_new_command(Command(script, stderr=stderr)) == new_command
