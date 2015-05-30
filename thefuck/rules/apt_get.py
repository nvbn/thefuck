from thefuck import shells
from thefuck.utils import sudo_support

try:
    import CommandNotFound
except ImportError:
    enabled_by_default = False

@sudo_support
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

@sudo_support
def get_new_command(command, settings):
    c = CommandNotFound.CommandNotFound()
    pkgs = c.getPackages(command.script.split(" ")[0])
    name, _ = pkgs[0]
    formatme = shells.and_('sudo apt-get install {}', '{}')
    return formatme.format(name, command.script)
