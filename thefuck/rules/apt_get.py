try:
    import CommandNotFound
except ImportError:
    enabled_by_default = False


def match(command, settings):
    if 'not found' in command.stderr:
        try:
            c = CommandNotFound.CommandNotFound()
            pkgs = c.getPackages(command.script.split(" ")[0])
            name, _ = pkgs[0]
            return True
        except IndexError:
            # IndexError is thrown when no matching package is found
            return False


def get_new_command(command, settings):
    c = CommandNotFound.CommandNotFound()
    pkgs = c.getPackages(command.script.split(" ")[0])
    name, _ = pkgs[0]
    return "sudo apt-get install {} && {}".format(name, command.script)
