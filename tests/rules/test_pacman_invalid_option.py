import pytest
from thefuck.rules.pacman_invalid_option import get_new_command, match
from thefuck.types import Command

good_output = """community/shared_meataxe 1.0-3
    A set of programs for working with matrix representations over finite fields
"""

bad_output = "error: invalid option '-"


@pytest.mark.parametrize("option", "SURQFDVT")
def test_not_match_good_output(option):
    assert not match(Command("pacman -{}s meat".format(option), good_output))


@pytest.mark.parametrize("option", "azxcbnm")
def test_not_match_bad_output(option):
    assert not match(Command("pacman -{}v meat".format(option), bad_output))


@pytest.mark.parametrize("option", "surqfdvt")
def test_match(option):
    assert match(Command("pacman -{}v meat".format(option), bad_output))


@pytest.mark.parametrize("option", "surqfdvt")
def test_get_new_command(option):
    new_command = get_new_command(Command("pacman -{}v meat".format(option), ""))
    assert new_command == "pacman -{}v meat".format(option.upper())
