from thefuck.utils import for_app, which

@for_app("choco", "cinst")
def match(command):
    return ((command.script.startswith('choco install') or 'cinst' in command.script_parts)
            and 'Installing the following packages' in command.output)


def get_new_command(command):
    # Find the argument that is the package name
    for script_part in command.script_parts:
        if script_part in ["choco", "cinst", "install"]:
            # Need exact match (bc chocolatey is a package)
            continue
        if script_part.startswith('-'):
            # Leading hyphens are parameters; some packages contain them though
            continue
        if '=' in script_part or '/' in script_part:
            # These are certainly parameters
            continue
        else:
            packageName = script_part
    # Find the name of the broken package, and append metapackage names
    if not packageName:
        return False
    return(command.script.replace(packageName, packageName + ".install"))


enabled_by_default = bool(which("choco")) or bool(which("cinst"))
