# Opens URL's in the default web browser
#
# Example:
# > open github.com
# The file ~/github.com does not exist.
# Perhaps you meant 'http://github.com'?
#
from thefuck.shells import shell
from thefuck.utils import eager, for_app


def is_arg_url(command):
    return ('.com' in command.script or
            '.edu' in command.script or
            '.info' in command.script or
            '.io' in command.script or
            '.ly' in command.script or
            '.me' in command.script or
            '.net' in command.script or
            '.org' in command.script or
            '.se' in command.script or
            'www.' in command.script)


@for_app('open', 'xdg-open', 'gnome-open', 'kde-open')
def match(command):
    return (is_arg_url(command) or
            command.stderr.strip().startswith('The file ') and
            command.stderr.strip().endswith(' does not exist.'))


@eager
def get_new_command(command):
    stderr = command.stderr.strip()
    if is_arg_url(command):
        yield command.script.replace('open ', 'open http://')
    elif stderr.startswith('The file ') and stderr.endswith(' does not exist.'):
        arg = command.script.split(' ', 1)[1]
        for option in ['touch', 'mkdir']:
            yield shell.and_(u'{} {}'.format(option, arg), command.script)
