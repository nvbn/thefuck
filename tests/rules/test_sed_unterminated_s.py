import pytest
from thefuck.rules.sed_unterminated_s import match, get_new_command
from tests.utils import Command


@pytest.fixture
def sed_unterminated_s():
    return "sed: -e expression #1, char 9: unterminated `s' command"


def test_match(sed_unterminated_s):
    assert match(Command('sed -e s/foo/bar', stderr=sed_unterminated_s), None)
    assert match(Command('sed -es/foo/bar', stderr=sed_unterminated_s), None)
    assert match(Command('sed -e s/foo/bar -e s/baz/quz', stderr=sed_unterminated_s), None)
    assert not match(Command('sed -e s/foo/bar'), None)
    assert not match(Command('sed -es/foo/bar'), None)
    assert not match(Command('sed -e s/foo/bar -e s/baz/quz'), None)


def test_get_new_command(sed_unterminated_s):
    assert get_new_command(Command('sed -e s/foo/bar', stderr=sed_unterminated_s), None) \
            == 'sed -e s/foo/bar/'
    assert get_new_command(Command('sed -es/foo/bar', stderr=sed_unterminated_s), None) \
            == 'sed -es/foo/bar/'
    assert get_new_command(Command(r"sed -e 's/\/foo/bar'", stderr=sed_unterminated_s), None) \
            == r"sed -e 's/\/foo/bar/'"
    assert get_new_command(Command(r"sed -e s/foo/bar -es/baz/quz", stderr=sed_unterminated_s), None) \
            == r"sed -e s/foo/bar/ -es/baz/quz/"
