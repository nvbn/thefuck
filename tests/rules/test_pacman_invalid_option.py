from thefuck.rules.pip_install import match, get_new_command
from thefuck.types import Command


def test_match():
    right_response = """
community/shared_meataxe 1.0-3
    A set of programs for working with matrix representations over finite fields
    """
    assert not match(Command('pacman -Ss meat', right_response))

    wrong_response = """
error: invalid option '-s'
    """
    assert match(Command('pacman -ss meat', wrong_response))

def test_get_new_command():
    assert get_new_command(Command('pacman -ss meat', '')) == 'pacman -Ss meat'
    assert get_new_command(Command('pacman -s meat', '')) == 'pacman -S meat'
