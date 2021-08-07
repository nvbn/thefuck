import pytest

from thefuck.rules.wrong_hyphen_before_subcommand import match, get_new_command
from thefuck.types import Command


@pytest.fixture(autouse=True)
def get_all_executables(mocker):
    mocker.patch(
        "thefuck.rules.wrong_hyphen_before_subcommand.get_all_executables",
        return_value=["git", "apt", "apt-get", "ls", "pwd"],
    )


@pytest.mark.parametrize("script", ["git-log", "apt-install python"])
def test_match(script):
    assert match(Command(script, ""))


@pytest.mark.parametrize("script", ["ls -la", "git2-make", "apt-get install python"])
def test_not_match(script):
    assert not match(Command(script, ""))


@pytest.mark.parametrize(
    "script, new_command",
    [("git-log", "git log"), ("apt-install python", "apt install python")],
)
def test_get_new_command(script, new_command):
    assert get_new_command(Command(script, "")) == new_command
