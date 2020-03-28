from thefuck.rules.pacman_invalid_option import get_new_command, match
from thefuck.types import Command

good_output = "community/shared_meataxe 1.0-3\n    A set of programs for working with matrix representations over finite fields\n    "

bad_output = "error: invalid option '-s'"


def test_match():
    assert not match(Command('pacman -Ss meat', good_output))
    assert not match(Command('sudo pacman -Ss meat', good_output))
    assert match(Command('pacman -ss meat', bad_output))
    assert match(Command('sudo pacman -ss meat', bad_output))


def test_get_new_command():
    new_command = get_new_command(Command('pacman -ss meat', bad_output))
    assert new_command == 'pacman -Ss meat'

    new_command = get_new_command(Command('sudo pacman -s meat', bad_output))
    assert new_command == 'sudo pacman -S meat'
