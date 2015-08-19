import pytest
from thefuck.rules.vagrant_up import match, get_new_command
from tests.utils import Command

@pytest.mark.parametrize('command', [
    Command(script='vagrant ssh', stderr='VM must be running to open SSH connection. Run `vagrant up`\nto start the virtual machine.'),
    Command(script='vagrant ssh devbox', stderr='VM must be running to open SSH connection. Run `vagrant up`\nto start the virtual machine.'),
    Command(script='vagrant rdp',
            stderr='VM must be created before running this command. Run `vagrant up` first.'),
    Command(script='vagrant rdp devbox',
            stderr='VM must be created before running this command. Run `vagrant up` first.')])
def test_match(command):
    assert match(command, None)


@pytest.mark.parametrize('command, new_command', [
    (Command(script='vagrant ssh', stderr='VM must be running to open SSH connection. Run `vagrant up`\nto start the virtual machine.'), 'vagrant up  && vagrant ssh'),
    (Command(script='vagrant ssh devbox', stderr='VM must be running to open SSH connection. Run `vagrant up`\nto start the virtual machine.'), 'vagrant up devbox && vagrant ssh devbox'),
    (Command(script='vagrant rdp',
            stderr='VM must be created before running this command. Run `vagrant up` first.'), 'vagrant up  && vagrant rdp'),
    (Command(script='vagrant rdp devbox',
            stderr='VM must be created before running this command. Run `vagrant up` first.'), 'vagrant up devbox && vagrant rdp devbox')])
def test_get_new_command(command, new_command):
    assert get_new_command(command, None) == new_command

