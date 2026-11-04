import pytest
from thefuck.rules.man import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('man read', ''),
    Command('man 2 read', ''),
    Command('man 3 read', ''),
    Command('man -s2 read', ''),
    Command('man -s3 read', ''),
    Command('man -s 2 read', ''),
    Command('man -s 3 read', '')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('man', ''),
    Command('man ', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('man read', ''), ['man 3 read', 'man 2 read', 'read --help']),
    (Command('man missing', "No manual entry for missing\n"), ['missing --help']),
    (Command('man 2 read', ''), 'man 3 read'),
    (Command('man 3 read', ''), 'man 2 read'),
    (Command('man -s2 read', ''), 'man -s3 read'),
    (Command('man -s3 read', ''), 'man -s2 read'),
    (Command('man -s 2 read', ''), 'man -s 3 read'),
    (Command('man -s 3 read', ''), 'man -s 2 read'),
    (Command('man python3', 'No manual entry for python3\n'),
     ['python3 --help']),
    (Command('man gcc-13', 'No manual entry for gcc-13\n'),
     ['gcc-13 --help']),
    (Command('man python3', ''),
     ['man 3 python3', 'man 2 python3', 'python3 --help']),
    (Command('man 3 foo3', ''), 'man 2 foo3'),
    (Command('man 2 foo2', ''), 'man 3 foo2'),
    (Command('man -s3 foo3', ''), 'man -s2 foo3'),
    (Command('man -s2 foo2', ''), 'man -s3 foo2'),
    (Command('man -s 3 foo3', ''), 'man -s 2 foo3'),
    (Command('man -s 2 foo2', ''), 'man -s 3 foo2'),
    (Command('man   3   foo3', ''), 'man   2   foo3'),
    (Command('man 3 "foo3"', ''), 'man 2 "foo3"'),
    (Command('/usr/bin/man 3 foo3', ''), '/usr/bin/man 2 foo3')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
