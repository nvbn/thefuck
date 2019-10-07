import pytest
from thefuck.rules.drmemory_no_dashdash import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('drmemory a.out', 'Usage: drmemory [options] --'),
    Command('/etc/bin/drmemory test.exe', 'Usage: drmemory [options] --'),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('drmemory -- a.out', ''),
    Command('/etc/bin/drmemory -- test.exe', ''),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('drmemory a.out', ''), 'drmemory -- a.out'),
    (Command('/etc/bin/drmemory test.exe', ''), '/etc/bin/drmemory -- test.exe'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
