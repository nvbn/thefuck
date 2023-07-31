from thefuck.specific.nix import nix_available
import subprocess

enabled_by_default = nix_available

# Set the priority just ahead of `fix_file` rule, which can generate low quality matches due
# to the sheer amount of paths in the nix store.
priority = 999


def get_nixpkgs_name(bin):
    """
    Returns the name of the Nix package that provides the given binary. It uses the
    `command-not-found` binary to do so, which is how nix-shell generates it's own suggestions.
    """

    result = subprocess.run(
        ["command-not-found", bin], stderr=subprocess.PIPE, universal_newlines=True
    )

    # return early if package is not available through nix
    if "nix-shell" not in result.stderr:
        return ""

    nixpkgs_name = result.stderr.split()[-1] if result.stderr.split() else ""
    return nixpkgs_name


def match(command):
    bin = command.script_parts[0]
    return (
        "nix-shell" not in command.script          # avoid recursion                                                # noqa: E501
        and "command not found" in command.output  # only match commands which had exit code: 127                   # noqa: E501
        and get_nixpkgs_name(bin)                  # only match commands which could be made available through nix  # noqa: E501
    )


def get_new_command(command):
    bin = command.script_parts[0]
    return 'nix-shell -p {0} --run "{1}"'.format(get_nixpkgs_name(bin), command.script)
