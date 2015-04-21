import sys

def match(command, settings):
    try:
        import CommandNotFound
        if 'not found' in command.stderr:
            try:
                c = CommandNotFound.CommandNotFound()
                pkgs = c.getPackages(command.script.split(" ")[0])
                name,_ = pkgs[0]
                return True
            except IndexError:
                # IndexError is thrown when no matching package is found
                return False
    except:
        return False

def get_new_command(command, settings):
    try:
        import CommandNotFound
        c = CommandNotFound.CommandNotFound()
        if 'not found' in command.stderr:
            pkgs = c.getPackages(command.script.split(" ")[0])
            name,_ = pkgs[0]
            return "sudo apt-get install %s" % name
    except:
        sys.stderr.write("Can't apt fuck\n")
        return ""
