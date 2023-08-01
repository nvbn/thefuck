import pytest
from thefuck.rules.nix_shell import get_nixpkgs_name, match, get_new_command
from thefuck.types import Command
from unittest.mock import patch, MagicMock


@pytest.mark.parametrize(
    "script,output,nixpkgs_name",
    [
        # output can be retrived by running `THEFUCK_DEBUG=true thefuck lsof`
        ("lsof", "/nix/store/p6dlr3skfhxpyphipg2bqnj52999banh-bash-5.2-p15/bin/sh: line 1: lsof: command not found", "lsof"),
    ],
)
def test_match(script, output, nixpkgs_name):
    with patch("thefuck.rules.nix_shell.get_nixpkgs_name") as mocked_get_nixpkgs_name:
        mocked_get_nixpkgs_name.return_value = nixpkgs_name
        command = Command(script, output)
        assert match(command)


@pytest.mark.parametrize(
    "script,output,nixpkgs_name",
    [
        # output can be retrived by running `THEFUCK_DEBUG=true thefuck foo`
        ("foo", "/nix/store/p6dlr3skfhxpyphipg2bqnj52999banh-bash-5.2-p15/bin/sh: line 1: foo: command not found", ""),
    ],
)
def test_not_match(script, output, nixpkgs_name):
    with patch("thefuck.rules.nix_shell.get_nixpkgs_name") as mocked_get_nixpkgs_name:
        mocked_get_nixpkgs_name.return_value = nixpkgs_name
        command = Command(script, output)
        assert not match(command)


@pytest.mark.parametrize(
    "script,nixpkgs_name,new_command",
    [
        ("lsof -i :3000", "lsof", 'nix-shell -p lsof --run "lsof -i :3000"'),
        ("xev", "xorg.xev", 'nix-shell -p xorg.xev --run "xev"'),
    ],
)
def test_get_new_command(script, nixpkgs_name, new_command):
    """Check that flags and params are preserved in the new command"""

    command = Command(script, "")
    with patch("thefuck.rules.nix_shell.get_nixpkgs_name") as mocked_get_nixpkgs_name:
        mocked_get_nixpkgs_name.return_value = nixpkgs_name
        assert get_new_command(command) == new_command


# Mocks the stderr of `command-not-found QUERY`. Mock values are retrieved by
# running `THEFUCK_DEBUG=true thefuck command-not-found lsof`.
mocked_cnf_stderr = {
    "lsof": "The program 'lsof' is not in your PATH. It is provided by several packages.\nYou can make it available in an ephemeral shell by typing one of the following:\n  nix-shell -p busybox\n  nix-shell -p lsof",
    "xev": "The program 'xev' is not in your PATH. You can make it available in an ephemeral shell by typing:\n  nix-shell -p xorg.xev",
    "foo": "foo: command not found",
}


@pytest.mark.parametrize(
    "bin,expected_nixpkgs_name,cnf_stderr",
    [
        ("lsof", "lsof", mocked_cnf_stderr["lsof"]),
        ("xev", "xorg.xev", mocked_cnf_stderr["xev"]),
        ("foo", "", mocked_cnf_stderr["foo"]),
    ],
)
def test_get_nixpkgs_name(bin, expected_nixpkgs_name, cnf_stderr):
    """Check that `get_nixpkgs_name` returns the correct name"""

    with patch("subprocess.run") as mocked_run:
        result = MagicMock()
        result.stderr = cnf_stderr
        mocked_run.return_value = result
        assert get_nixpkgs_name(bin) == expected_nixpkgs_name
