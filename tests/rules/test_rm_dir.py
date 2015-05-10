import pytest
from thefuck.rules.rm_dir import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command('rm foo', stderr='rm: foo: is a directory'),
    Command('rm foo', stderr='rm: foo: Is a directory')])
def test_match(command):
    assert match(command, None)
    assert match(command, None)


@pytest.mark.parametrize('command', [
    Command('rm foo'), Command('rm foo'), Command()])
def test_not_match(command):
    assert not match(command, None)


def test_get_new_command():
    assert get_new_command(Command('rm foo', '', ''), None) == 'rm -rf foo'
