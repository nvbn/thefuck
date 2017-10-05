import re
from thefuck.specific.sudo import sudo_support
from thefuck.utils import for_app, replace_command

dnf_commands = [
    'autoremove',
    'check',
    'check-update',
    'clean',
    'deplist',
    'distro-sync',
    'downgrade',
    'group',
    'help',
    'history',
    'info',
    'install',
    'list',
    'makecache',
    'mark',
    'provides',
    'reinstall',
    'remove',
    'repolist',
    'repoquery',
    'repository-packages',
    'search',
    'shell',
    'swap',
    'updateinfo',
    'upgrade',
    'upgrade-minimal'
]

regex = re.compile(r'No such command: (.*)\.')


@for_app('dnf')
@sudo_support
def match(command):
    return 'no such command' in command.output.lower()


@sudo_support
def get_new_command(command):
    misspelled_command = regex.findall(command.output)[0]
    return replace_command(command, misspelled_command, dnf_commands)


enabled_by_default = True
