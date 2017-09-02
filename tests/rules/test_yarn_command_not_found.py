# -*- encoding: utf-8 -*-

from io import BytesIO
import pytest
from thefuck.types import Command
from thefuck.rules.yarn_command_not_found import match, get_new_command

output = '''
error Command "{}" not found.
'''.format

yarn_help_stdout = b'''

  Usage: yarn [command] [flags]

  Options:

    -h, --help                      output usage information
    -V, --version                   output the version number
    --verbose                       output verbose messages on internal operations
    --offline                       trigger an error if any required dependencies are not available in local cache
    --prefer-offline                use network only if dependencies are not available in local cache
    --strict-semver                 
    --json                          
    --ignore-scripts                don't run lifecycle scripts
    --har                           save HAR output of network traffic
    --ignore-platform               ignore platform checks
    --ignore-engines                ignore engines check
    --ignore-optional               ignore optional dependencies
    --force                         ignore all caches
    --no-bin-links                  don't generate bin links when setting up packages
    --flat                          only allow one version of a package
    --prod, --production [prod]     
    --no-lockfile                   don't read or generate a lockfile
    --pure-lockfile                 don't generate a lockfile
    --frozen-lockfile               don't generate a lockfile and fail if an update is needed
    --link-duplicates               create hardlinks to the repeated modules in node_modules
    --global-folder <path>          
    --modules-folder <path>         rather than installing modules into the node_modules folder relative to the cwd, output them here
    --cache-folder <path>           specify a custom folder to store the yarn cache
    --mutex <type>[:specifier]      use a mutex to ensure only one yarn instance is executing
    --no-emoji                      disable emoji in output
    --proxy <host>                  
    --https-proxy <host>            
    --no-progress                   disable progress bar
    --network-concurrency <number>  maximum number of concurrent network requests

  Commands:

    - access
    - add
    - bin
    - cache
    - check
    - clean
    - config
    - generate-lock-entry
    - global
    - import
    - info
    - init
    - install
    - licenses
    - link
    - list
    - login
    - logout
    - outdated
    - owner
    - pack
    - publish
    - remove
    - run
    - tag
    - team
    - unlink
    - upgrade
    - upgrade-interactive
    - version
    - versions
    - why

  Run `yarn help COMMAND` for more information on specific commands.
  Visit https://yarnpkg.com/en/docs/cli/ to learn more about Yarn.
''' # noqa


@pytest.fixture(autouse=True)
def yarn_help(mocker):
    patch = mocker.patch('thefuck.rules.yarn_command_not_found.Popen')
    patch.return_value.stdout = BytesIO(yarn_help_stdout)
    return patch


@pytest.mark.parametrize('command', [
    Command('yarn whyy webpack', output('whyy'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('npm nuild', output('nuild')),
    Command('yarn install', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, result', [
    (Command('yarn whyy webpack', output('whyy')),
     'yarn why webpack'),
    (Command('yarn require lodash', output('require')),
     'yarn add lodash')])
def test_get_new_command(command, result):
    fixed_command = get_new_command(command)
    if isinstance(fixed_command, list):
        fixed_command = fixed_command[0]

    assert fixed_command == result
