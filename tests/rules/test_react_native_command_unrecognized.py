import pytest
from io import BytesIO
from thefuck.rules.react_native_command_unrecognized import match, \
    get_new_command
from thefuck.types import Command

output = "Unrecognized command '{}'".format

stdout = b'''
Scanning 615 folders for symlinks in /home/nvbn/work/zcho/BookkaWebView/node_modules (6ms)

  Usage: react-native [options] [command]


  Options:

    -V, --version  output the version number
    -h, --help     output usage information


  Commands:

    start [options]                    starts the webserver
    run-ios [options]                  builds your app and starts it on iOS simulator
    run-android [options]              builds your app and starts it on a connected Android emulator or device
    new-library [options]              generates a native library bridge
    bundle [options]                   builds the javascript bundle for offline use
    unbundle [options]                 builds javascript as "unbundle" for offline use
    eject [options]                    Re-create the iOS and Android folders and native code
    link [options] [packageName]       links all native dependencies (updates native build files)
    unlink [options] <packageName>     unlink native dependency
    install [options] <packageName>    install and link native dependencies
    uninstall [options] <packageName>  uninstall and unlink native dependencies
    upgrade [options]                  upgrade your app's template files to the latest version; run this after updating the react-native version in your package.json and running npm install
    log-android [options]              starts adb logcat
    log-ios [options]                  starts iOS device syslog tail
'''


@pytest.mark.parametrize('command', [
    Command('react-native star', output('star')),
    Command('react-native android-logs', output('android-logs'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('gradle star', output('star')),
    Command('react-native start', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, result', [
    (Command('react-native star', output('star')),
     'react-native start'),
    (Command('react-native logsandroid -f', output('logsandroid')),
     'react-native log-android -f')])
def test_get_new_command(mocker, command, result):
    patch = mocker.patch(
        'thefuck.rules.react_native_command_unrecognized.Popen')
    patch.return_value.stdout = BytesIO(stdout)
    assert get_new_command(command)[0] == result
