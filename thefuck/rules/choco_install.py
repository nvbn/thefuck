from thefuck.utils import for_app, which


@for_app("choco", "cinst")
def match(command):
    return ((command.script.startswith('choco install') or 'cinst' in command.script_parts)
            and 'Installing the following packages' in command.output)


def get_new_command(command):
    # Find the argument that is the package name
    for script_part in command.script_parts:
        if (
            script_part not in ["choco", "cinst", "install"]
            # Need exact match (bc chocolatey is a package)
            and not script_part.startswith('-')
            # Leading hyphens are parameters; some packages contain them though
            and '=' not in script_part and '/' not in script_part
            # These are certainly parameters
        ):
            return command.script.replace(script_part, script_part + ".install")
    return []


enabled_by_default = bool(which("choco")) or bool(which("cinst"))
