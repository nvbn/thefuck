import pytest
from thefuck.rules.cp_create_destination import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize(
    "script, output",
    [("cp", "cp: directory foo does not exist\n"), ("mv", "No such file or directory")],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output", [("cp", ""), ("mv", ""), ("ls", "No such file or directory")]
)
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        ("cp foo bar/", "cp: directory foo does not exist\n", "mkdir -p bar/ && cp foo bar/"),
        ("mv foo bar/", "No such file or directory", "mkdir -p bar/ && mv foo bar/"),
        ("cp foo bar/baz/", "cp: directory foo does not exist\n", "mkdir -p bar/baz/ && cp foo bar/baz/"),
    ],
)
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
