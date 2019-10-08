from io import BytesIO

import pytest

from thefuck.rules.yum_invalid_operation import match, get_new_command, _get_operations
from thefuck.types import Command

yum_help_text = '''Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
Usage: yum [options] COMMAND

List of Commands:

check          Check for problems in the rpmdb
check-update   Check for available package updates
clean          Remove cached data
deplist        List a package's dependencies
distribution-synchronization Synchronize installed packages to the latest available versions
downgrade      downgrade a package
erase          Remove a package or packages from your system
fs             Acts on the filesystem data of the host, mainly for removing docs/lanuages for minimal hosts.
fssnapshot     Creates filesystem snapshots, or lists/deletes current snapshots.
groups         Display, or use, the groups information
help           Display a helpful usage message
history        Display, or use, the transaction history
info           Display details about a package or group of packages
install        Install a package or packages on your system
langavailable  Check available languages
langinfo       List languages information
langinstall    Install appropriate language packs for a language
langlist       List installed languages
langremove     Remove installed language packs for a language
list           List a package or groups of packages
load-transaction load a saved transaction from filename
makecache      Generate the metadata cache
provides       Find what package provides the given value
reinstall      reinstall a package
repo-pkgs      Treat a repo. as a group of packages, so we can install/remove all of them
repolist       Display the configured software repositories
search         Search package details for the given string
shell          Run an interactive yum shell
swap           Simple way to swap packages, instead of using shell
update         Update a package or packages on your system
update-minimal Works like upgrade, but goes to the 'newest' package match which fixes a problem that affects your system
updateinfo     Acts on repository update information
upgrade        Update packages taking obsoletes into account
version        Display a version for the machine and/or available repos.


Options:
  -h, --help            show this help message and exit
  -t, --tolerant        be tolerant of errors
  -C, --cacheonly       run entirely from system cache, don't update cache
  -c [config file], --config=[config file]
                        config file location
  -R [minutes], --randomwait=[minutes]
                        maximum command wait time
  -d [debug level], --debuglevel=[debug level]
                        debugging output level
  --showduplicates      show duplicates, in repos, in list/search commands
  -e [error level], --errorlevel=[error level]
                        error output level
  --rpmverbosity=[debug level name]
                        debugging output level for rpm
  -q, --quiet           quiet operation
  -v, --verbose         verbose operation
  -y, --assumeyes       answer yes for all questions
  --assumeno            answer no for all questions
  --version             show Yum version and exit
  --installroot=[path]  set install root
  --enablerepo=[repo]   enable one or more repositories (wildcards allowed)
  --disablerepo=[repo]  disable one or more repositories (wildcards allowed)
  -x [package], --exclude=[package]
                        exclude package(s) by name or glob
  --disableexcludes=[repo]
                        disable exclude from main, for a repo or for
                        everything
  --disableincludes=[repo]
                        disable includepkgs for a repo or for everything
  --obsoletes           enable obsoletes processing during updates
  --noplugins           disable Yum plugins
  --nogpgcheck          disable gpg signature checking
  --disableplugin=[plugin]
                        disable plugins by name
  --enableplugin=[plugin]
                        enable plugins by name
  --skip-broken         skip packages with depsolving problems
  --color=COLOR         control whether color is used
  --releasever=RELEASEVER
                        set value of $releasever in yum config and repo files
  --downloadonly        don't update, just download
  --downloaddir=DLDIR   specifies an alternate directory to store packages
  --setopt=SETOPTS      set arbitrary config and repo options
  --bugfix              Include bugfix relevant packages, in updates
  --security            Include security relevant packages, in updates
  --advisory=ADVS, --advisories=ADVS
                        Include packages needed to fix the given advisory, in
                        updates
  --bzs=BZS             Include packages needed to fix the given BZ, in
                        updates
  --cves=CVES           Include packages needed to fix the given CVE, in
                        updates
  --sec-severity=SEVS, --secseverity=SEVS
                        Include security relevant packages matching the
                        severity, in updates

  Plugin Options:
    --samearch-priorities
                        Priority-exclude packages based on name + arch
'''
yum_unsuccessful_search_text = '''Warning: No matches found for: {}
No matches found
'''
yum_successful_vim_search_text = '''================================================== N/S matched: vim ===================================================
protobuf-vim.x86_64 : Vim syntax highlighting for Google Protocol Buffers descriptions
vim-X11.x86_64 : The VIM version of the vi editor for the X Window System - GVim
vim-common.x86_64 : The common files needed by any version of the VIM editor
vim-enhanced.x86_64 : A version of the VIM editor which includes recent enhancements
vim-filesystem.x86_64 : VIM filesystem layout
vim-filesystem.noarch : VIM filesystem layout
vim-minimal.x86_64 : A minimal version of the VIM editor

  Name and summary matches only, use "search all" for everything.
'''

yum_invalid_op_text = '''Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
No such command: {}. Please use /usr/bin/yum --help
'''

yum_operations = [
    'check', 'check-update', 'clean', 'deplist', 'distribution-synchronization', 'downgrade', 'erase', 'fs',
    'fssnapshot', 'groups', 'help', 'history', 'info', 'install', 'langavailable', 'langinfo', 'langinstall',
    'langlist', 'langremove', 'list', 'load-transaction', 'makecache', 'provides', 'reinstall', 'repo-pkgs', 'repolist',
    'search', 'shell', 'swap', 'update', 'update-minimal', 'updateinfo', 'upgrade', 'version', ]


@pytest.mark.parametrize('command', [
    'saerch', 'uninstall',
])
def test_match(command):
    assert match(Command('yum {}'.format(command), yum_invalid_op_text.format(command)))


@pytest.mark.parametrize('command, output', [
    ('vim', ''),
    ('yum', yum_help_text,),
    ('yum help', yum_help_text,),
    ('yum search asdf', yum_unsuccessful_search_text.format('asdf'),),
    ('yum search vim', yum_successful_vim_search_text)
])
def test_not_match(command, output):
    assert not match(Command(command, output))


@pytest.fixture
def yum_help(mocker):
    mock = mocker.patch('subprocess.Popen')
    mock.return_value.stdout = BytesIO(bytes(yum_help_text.encode('utf-8')))
    return mock


@pytest.mark.usefixtures('no_memoize', 'yum_help')
def test_get_operations():
    assert _get_operations() == yum_operations


@pytest.mark.usefixtures('no_memoize', 'yum_help')
@pytest.mark.parametrize('script, output, result', [
    ('yum uninstall', yum_invalid_op_text.format('uninstall'), 'yum remove',),
    ('yum saerch asdf', yum_invalid_op_text.format('saerch'), 'yum search asdf',),
    ('yum hlep', yum_invalid_op_text.format('hlep'), 'yum help',),
])
def test_get_new_command(script, output, result):
    assert get_new_command(Command(script, output))[0] == result
