import pytest
from thefuck.rules.long_form_help import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('output', [
    'Try \'grep --help\' for more information.'])
def test_match(output):
    assert match(Command('grep -h', output))


def test_not_match():
    assert not match(Command('', ''))


@pytest.mark.parametrize('before, after', [
    ('grep -h', 'grep --help'),
    ('tar -h', 'tar --help'),
    ('docker run -h', 'docker run --help'),
    ('cut -h', 'cut --help')])
def test_get_new_command(before, after):
    assert get_new_command(Command(before, '')) == after
