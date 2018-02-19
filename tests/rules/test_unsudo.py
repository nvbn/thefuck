import pytest
from thefuck.rules.unsudo import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('output', [
    'you cannot perform this operation as root'])
def test_match(output):
    assert match(Command('sudo ls', output))


def test_not_match():
    assert not match(Command('', ''))
    assert not match(Command('sudo ls', 'Permission denied'))
    assert not match(Command('ls', 'you cannot perform this operation as root'))


@pytest.mark.parametrize('before, after', [
    ('sudo ls', 'ls'),
    ('sudo pacaur -S helloworld', 'pacaur -S helloworld')])
def test_get_new_command(before, after):
    assert get_new_command(Command(before, '')) == after
