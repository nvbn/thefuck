from thefuck.specific.apt import apt_available
from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app

enabled_by_default = apt_available


@sudo_support
@for_app('apt')
def match(command):
    return 'apt list --upgradable' in command.output


@sudo_support
def get_new_command(command):
    return 'apt list --upgradable'
