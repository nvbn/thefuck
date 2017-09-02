import pytest
from six import BytesIO
from thefuck.rules.gem_unknown_command import match, get_new_command
from thefuck.types import Command

output = '''
ERROR:  While executing gem ... (Gem::CommandLineError)
    Unknown command {}
'''

gem_help_commands_stdout = b'''
GEM commands are:

    build             Build a gem from a gemspec
    cert              Manage RubyGems certificates and signing settings
    check             Check a gem repository for added or missing files
    cleanup           Clean up old versions of installed gems
    contents          Display the contents of the installed gems
    dependency        Show the dependencies of an installed gem
    environment       Display information about the RubyGems environment
    fetch             Download a gem and place it in the current directory
    generate_index    Generates the index files for a gem server directory
    help              Provide help on the 'gem' command
    install           Install a gem into the local repository
    list              Display local gems whose name matches REGEXP
    lock              Generate a lockdown list of gems
    mirror            Mirror all gem files (requires rubygems-mirror)
    open              Open gem sources in editor
    outdated          Display all gems that need updates
    owner             Manage gem owners of a gem on the push server
    pristine          Restores installed gems to pristine condition from files
                      located in the gem cache
    push              Push a gem up to the gem server
    query             Query gem information in local or remote repositories
    rdoc              Generates RDoc for pre-installed gems
    search            Display remote gems whose name matches REGEXP
    server            Documentation and gem repository HTTP server
    sources           Manage the sources and cache file RubyGems uses to search
                      for gems
    specification     Display gem specification (in yaml)
    stale             List gems along with access times
    uninstall         Uninstall gems from the local repository
    unpack            Unpack an installed gem to the current directory
    update            Update installed gems to the latest version
    which             Find the location of a library file you can require
    yank              Remove a pushed gem from the index

For help on a particular command, use 'gem help COMMAND'.

Commands may be abbreviated, so long as they are unambiguous.
e.g. 'gem i rake' is short for 'gem install rake'.

'''


@pytest.fixture(autouse=True)
def gem_help_commands(mocker):
    patch = mocker.patch('subprocess.Popen')
    patch.return_value.stdout = BytesIO(gem_help_commands_stdout)
    return patch


@pytest.mark.parametrize('script, command', [
    ('gem isntall jekyll', 'isntall'),
    ('gem last --local', 'last')])
def test_match(script, command):
    assert match(Command(script, output.format(command)))


@pytest.mark.parametrize('script, output', [
    ('gem install jekyll', ''),
    ('git log', output.format('log'))])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, output, result', [
    ('gem isntall jekyll', output.format('isntall'), 'gem install jekyll'),
    ('gem last --local', output.format('last'), 'gem list --local')])
def test_get_new_command(script, output, result):
    new_command = get_new_command(Command(script, output))
    assert new_command[0] == result
