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
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='vagrant ssh', stderr=''),
    Command(script='vagrant ssh jeff', stderr='The machine with the name \'jeff\' was not found configured for this Vagrant environment.'),
    Command(script='vagrant ssh', stderr='A Vagrant environment or target machine is required to run this command. Run `vagrant init` to create a new Vagrant environment. Or, get an ID of a target machine from `vagrant global-status` to run this command on. A final option is to change to a directory with a Vagrantfile and to try again.'),
    Command()])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command(script='vagrant ssh', stderr='VM must be running to open SSH connection. Run `vagrant up`\nto start the virtual machine.'), 'vagrant up && vagrant ssh'),
    (Command(script='vagrant ssh devbox', stderr='VM must be running to open SSH connection. Run `vagrant up`\nto start the virtual machine.'), ['vagrant up devbox && vagrant ssh devbox', 'vagrant up && vagrant ssh devbox']),
    (Command(script='vagrant rdp',
            stderr='VM must be created before running this command. Run `vagrant up` first.'), 'vagrant up && vagrant rdp'),
    (Command(script='vagrant rdp devbox',
            stderr='VM must be created before running this command. Run `vagrant up` first.'), ['vagrant up devbox && vagrant rdp devbox', 'vagrant up && vagrant rdp devbox'])])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
