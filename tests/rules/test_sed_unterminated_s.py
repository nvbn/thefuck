import pytest
from thefuck.rules.sed_unterminated_s import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def sed_unterminated_s():
    return "sed: -e expression #1, char 9: unterminated `s' command"


def test_match(sed_unterminated_s):
    assert match(Command('sed -e s/foo/bar', sed_unterminated_s))
    assert match(Command('sed -es/foo/bar', sed_unterminated_s))
    assert match(Command('sed -e s/foo/bar -e s/baz/quz', sed_unterminated_s))
    assert not match(Command('sed -e s/foo/bar', ''))
    assert not match(Command('sed -es/foo/bar', ''))
    assert not match(Command('sed -e s/foo/bar -e s/baz/quz', ''))


def test_get_new_command(sed_unterminated_s):
    assert (get_new_command(Command('sed -e s/foo/bar', sed_unterminated_s))
            == 'sed -e s/foo/bar/')
    assert (get_new_command(Command('sed -es/foo/bar', sed_unterminated_s))
            == 'sed -es/foo/bar/')
    assert (get_new_command(Command(r"sed -e 's/\/foo/bar'", sed_unterminated_s))
            == r"sed -e 's/\/foo/bar/'")
    assert (get_new_command(Command(r"sed -e s/foo/bar -es/baz/quz", sed_unterminated_s))
            == r"sed -e s/foo/bar/ -es/baz/quz/")
