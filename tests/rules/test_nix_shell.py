import pytest
from thefuck.rules.nix_shell import get_nixpkgs_name, get_new_command
from thefuck.types import Command
from unittest.mock import patch

mocked_nixpkgs = {
    "lsof": "The program 'lsof' is not in your PATH. It is provided by several packages.\nYou can make it available in an ephemeral shell by typing one of the following:\n  nix-shell -p busybox\n  nix-shell -p lsof",
    "xev": "The program 'xev' is not in your PATH. You can make it available in an ephemeral shell by typing:\n  nix-shell -p xorg.xev",
    "foo": "foo: command not found",
}


@pytest.mark.parametrize(
    "command, output", [("lsof", "lsof"), ("xev", "xorg.xev"), ("foo", "")]
)
def test_get_nixpkgs_name(command, output):
    """Check that `get_nixpkgs_name` returns the correct name"""

    with patch("subprocess.run") as mocked_run:
        instance = mocked_run.return_value
        instance.stderr = mocked_nixpkgs[command]
        assert get_nixpkgs_name(command) == output


# check that flags and params are preserved for the new command
@pytest.mark.parametrize(
    "command_script, new_command",
    [
        ("lsof -i :3000", 'nix-shell -p lsof --run "lsof -i :3000"'),
        ("xev", 'nix-shell -p xorg.xev --run "xev"'),
    ],
)
def test_get_new_command(command_script, new_command):
    """Check that flags and params are preserved in the new command"""

    command = Command(command_script, "")
    with patch("subprocess.run") as mocked_run:
        instance = mocked_run.return_value
        instance.stderr = mocked_nixpkgs[command.script_parts[0]]
        assert get_new_command(command) == new_command
