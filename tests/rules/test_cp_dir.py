import pytest
from thefuck.rules.cp_dir import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command('cp foo foo_copy', stderr='cp: foo: is a directory'),
    Command('cp bar bar_copy', stderr='cp: bar: Is a directory'),
    Command('sudo cp qux qux_copy', stderr='cp: qux: is a directory')])
def test_match(command):
    assert match(command, None)


@pytest.mark.parametrize('command', [
    Command('cp foo foo_copy'), Command('cp foo foo_copy'), Command()])
def test_not_match(command):
    assert not match(command, None)


def test_get_new_command():
    assert get_new_command(
        Command('cp foo foo_copy', '', ''), None) == 'cp -r foo foo_copy'
