# Opens URL's in the default web browser
#
# Example:
# > open github.com
# The file ~/github.com does not exist.
# Perhaps you meant 'http://github.com'?
#
from thefuck.utils import for_app


@for_app('open', 'xdg-open', 'gnome-open', 'kde-open')
def match(command):
    return ('.com' in command.script
            or '.net' in command.script
            or '.org' in command.script
            or '.ly' in command.script
            or '.io' in command.script
            or '.se' in command.script
            or '.edu' in command.script
            or '.info' in command.script
            or '.me' in command.script
            or 'www.' in command.script)


def get_new_command(command):
    return command.script.replace('open ', 'open http://')
