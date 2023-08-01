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

    # The suggestion, if any, will be found in stderr. Upstream definition: https://github.com/NixOS/nixpkgs/blob/b6fbd87328f8eabd82d65cc8f75dfb74341b0ace/nixos/modules/programs/command-not-found/command-not-found.nix#L48-L90
    text = result.stderr

    # return early if binary is not available through nix
    if "nix-shell" not in text:
        return ""

    nixpkgs_name = text.split()[-1] if text.split() else ""
    return nixpkgs_name


def match(command):
    bin = command.script_parts[0]
    return (
        "command not found" in command.output  # only match commands which had exit code: 127                   # noqa: E501
        and get_nixpkgs_name(bin)              # only match commands which could be made available through nix  # noqa: E501
    )


def get_new_command(command):
    bin = command.script_parts[0]
    return 'nix-shell -p {0} --run "{1}"'.format(get_nixpkgs_name(bin), command.script)
