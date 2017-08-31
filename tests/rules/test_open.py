import pytest
from thefuck.rules.open import is_arg_url, match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output(script):
    return 'The file {} does not exist.\n'.format(script.split(' ', 1)[1])


@pytest.mark.parametrize('script', [
    'open foo.com',
    'open foo.edu',
    'open foo.info',
    'open foo.io',
    'open foo.ly',
    'open foo.me',
    'open foo.net',
    'open foo.org',
    'open foo.se',
    'open www.foo.ru'])
def test_is_arg_url(script):
    assert is_arg_url(Command(script, ''))


@pytest.mark.parametrize('script', ['open foo', 'open bar.txt', 'open egg.doc'])
def test_not_is_arg_url(script):
    assert not is_arg_url(Command(script, ''))


@pytest.mark.parametrize('script', [
    'open foo.com',
    'xdg-open foo.com',
    'gnome-open foo.com',
    'kde-open foo.com',
    'open nonest'])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, new_command', [
    ('open foo.io', ['open http://foo.io']),
    ('xdg-open foo.io', ['xdg-open http://foo.io']),
    ('gnome-open foo.io', ['gnome-open http://foo.io']),
    ('kde-open foo.io', ['kde-open http://foo.io']),
    ('open nonest', ['touch nonest && open nonest',
                     'mkdir nonest && open nonest'])])
def test_get_new_command(script, new_command, output):
    assert get_new_command(Command(script, output)) == new_command
