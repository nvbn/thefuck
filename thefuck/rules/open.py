# Opens URL's in the default web browser
#
# Example:
# > open github.com
# The file ~/github.com does not exist.
# Perhaps you meant 'http://github.com'?
#


def match(command, settings):
    return (command.script.startswith(('open', 'xdg-open', 'gnome-open', 'kde-open'))
            and (
                '.com' in command.script
                or '.net' in command.script
                or '.org' in command.script
                or '.ly' in command.script
                or '.io' in command.script
                or '.se' in command.script
                or '.edu' in command.script
                or '.info' in command.script
                or '.me' in command.script
                or 'www.' in command.script))


def get_new_command(command, settings):
    return command.script.replace('open ', 'open http://')
