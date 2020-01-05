import pytest
from thefuck.rules.choco_install import match, get_new_command
from thefuck.types import Command


package_not_found_error = (
    'Chocolatey v0.10.15\n'
    'Installing the following packages:\n'
    'logstitcher\n'
    'By installing you accept licenses for the packages.\n'
    'logstitcher not installed. The package was not found with the source(s) listed.\n'
    ' Source(s): \'https://chocolatey.org/api/v2/\'\n'
    ' NOTE: When you specify explicit sources, it overrides default sources.\n'
    'If the package version is a prerelease and you didn\'t specify `--pre`,\n'
    ' the package may not be found.\n'
    'Please see https://chocolatey.org/docs/troubleshooting for more\n'
    ' assistance.\n'
    '\n'
    'Chocolatey installed 0/1 packages. 1 packages failed.\n'
    ' See the log for details (C:\\ProgramData\\chocolatey\\logs\\chocolatey.log).\n'
    '\n'
    'Failures\n'
    ' - logstitcher - logstitcher not installed. The package was not found with the source(s) listed.\n'
    ' Source(s): \'https://chocolatey.org/api/v2/\'\n'
    ' NOTE: When you specify explicit sources, it overrides default sources.\n'
    'If the package version is a prerelease and you didn\'t specify `--pre`,\n'
    ' the package may not be found.\n'
    'Please see https://chocolatey.org/docs/troubleshooting for more\n'
    ' assistance.\n'
)


@pytest.mark.parametrize('command', [
    Command('choco install logstitcher', package_not_found_error),
    Command('cinst logstitcher', package_not_found_error),
    Command('choco install logstitcher -y', package_not_found_error),
    Command('cinst logstitcher -y', package_not_found_error),
    Command('choco install logstitcher -y -n=test', package_not_found_error),
    Command('cinst logstitcher -y -n=test', package_not_found_error),
    Command('choco install logstitcher -y -n=test /env', package_not_found_error),
    Command('cinst logstitcher -y -n=test /env', package_not_found_error),
    Command('choco install chocolatey -y', package_not_found_error),
    Command('cinst chocolatey -y', package_not_found_error)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('choco /?', ''),
    Command('choco upgrade logstitcher', ''),
    Command('cup logstitcher', ''),
    Command('choco upgrade logstitcher -y', ''),
    Command('cup logstitcher -y', ''),
    Command('choco upgrade logstitcher -y -n=test', ''),
    Command('cup logstitcher -y -n=test', ''),
    Command('choco upgrade logstitcher -y -n=test /env', ''),
    Command('cup logstitcher -y -n=test /env', ''),
    Command('choco upgrade chocolatey -y', ''),
    Command('cup chocolatey -y', ''),
    Command('choco uninstall logstitcher', ''),
    Command('cuninst logstitcher', ''),
    Command('choco uninstall logstitcher -y', ''),
    Command('cuninst logstitcher -y', ''),
    Command('choco uninstall logstitcher -y -n=test', ''),
    Command('cuninst logstitcher -y -n=test', ''),
    Command('choco uninstall logstitcher -y -n=test /env', ''),
    Command('cuninst logstitcher -y -n=test /env', ''),
    Command('choco uninstall chocolatey -y', ''),
    Command('cuninst chocolatey -y', '')])
def not_test_match(command):
    assert not match(command)


@pytest.mark.parametrize('before, after', [
    ('choco install logstitcher', 'choco install logstitcher.install'),
    ('cinst logstitcher', 'cinst logstitcher.install'),
    ('choco install logstitcher -y', 'choco install logstitcher.install -y'),
    ('cinst logstitcher -y', 'cinst logstitcher.install -y'),
    ('choco install logstitcher -y -n=test', 'choco install logstitcher.install -y -n=test'),
    ('cinst logstitcher -y -n=test', 'cinst logstitcher.install -y -n=test'),
    ('choco install logstitcher -y -n=test /env', 'choco install logstitcher.install -y -n=test /env'),
    ('cinst logstitcher -y -n=test /env', 'cinst logstitcher.install -y -n=test /env'),
    ('choco install chocolatey -y', 'choco install chocolatey.install -y'),
    ('cinst chocolatey -y', 'cinst chocolatey.install -y'), ])
def test_get_new_command(before, after):
    assert (get_new_command(Command(before, '')) == after)
