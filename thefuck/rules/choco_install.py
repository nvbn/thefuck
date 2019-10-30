from thefuck.utils import for_app


@for_app("choco", "cinst")
def match(command):
    return ((command.script.startswith('choco install') or 'cinst' in command.script_parts)
            and 'Installing the following packages' in command.output)


def get_new_command(command):
    # Find the argument that is the package name
    for script_part in command.script_parts:
        if "choco" in i:
            continue
        if "cinst" in i:
            continue
        if "install" in i:
            continue
        if i.startswith('-'):   # Some parameters start with hyphens; some packages contain them though
            continue
        if '=' in i:            # Some paramaters contain '='
            continue
        if '/' in i:            # Some parameters contain slashes
            continue
        else:
            packageName = i
    # Find the name of the broken package, and append metapackage names
    if not packageName:
        return False
    return(command.script.replace(packageName, packageName + ".install"))


enabled_by_default = bool(which("choco")) or bool(which("cinst"))
