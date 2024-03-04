import pytest
from thefuck.rules.su import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('output', [
    'command not found: sudo'])
def test_match(output):
    assert match(Command('', output))


def test_not_match():
    assert not match(Command('', ''))
    assert not match(Command('sudo ls', 'Permission denied'))
    assert not match(Command('su -c ls', 'Permission denied'))
    assert not match(Command('ls', 'command not found: ls'))


@pytest.mark.parametrize('before, after', [
    ('sudo ls', 'su -c "ls"'),
    ('sudo echo a > b', 'su -c "echo a > b"'),
    ('sudo echo "a" >> b', 'su -c "echo \\"a\\" >> b"'),
    ('sudo mkdir && touch a', 'su -c "mkdir && touch a"')])
def test_get_new_command(before, after):
    assert get_new_command(Command(before, '')) == after
