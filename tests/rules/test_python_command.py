from thefuck.main import Command
from thefuck.rules.sudo import match, get_new_command

def test_match():
    assert match(Command('', '', 'Permission denied'), None)
    assert not match(Command('', '', ''), None)

def test_get_new_command():
    assert get_new_command(Command('./test_sudo.py', '', ''), None) == 'python ./test_sudo.py'
