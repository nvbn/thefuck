import pytest
from thefuck.rules.nixos_cmd_not_found import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('vim', 'nix-env -iA nixos.vim')])
def test_match(mocker, command):
    mocker.patch('thefuck.rules.nixos_cmd_not_found', return_value=None)
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('vim', ''),
    Command('', '')])
def test_not_match(mocker, command):
    mocker.patch('thefuck.rules.nixos_cmd_not_found', return_value=None)
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('vim', 'nix-env -iA nixos.vim'), 'nix-env -iA nixos.vim && vim'),
    (Command('pacman', 'nix-env -iA nixos.pacman'), 'nix-env -iA nixos.pacman && pacman')])
def test_get_new_command(mocker, command, new_command):
    assert get_new_command(command) == new_command
