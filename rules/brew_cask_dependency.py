from thefuck.utils import for_app, eager
from thefuck.shells import shell
from thefuck.specific.brew import brew_available


@for_app('brew')
def match(command):
    return (u'install' in command.script_parts
            and u'brew cask install' in command.output)


@eager
def _get_cask_install_lines(output):
    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('brew cask install'):
            yield line


def _get_script_for_brew_cask(output):
    cask_install_lines = _get_cask_install_lines(output)
    if len(cask_install_lines) > 1:
        return shell.and_(*cask_install_lines)
    else:
        return cask_install_lines[0]


def get_new_command(command):
    brew_cask_script = _get_script_for_brew_cask(command.output)
    return shell.and_(brew_cask_script, command.script)


enabled_by_default = brew_available
