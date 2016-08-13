import pytest
from thefuck.rules.react_native_command_unrecognized import match, \
    get_new_command
from tests.utils import Command

stderr = 'Command `{}` unrecognized'.format

stdout = '''
Usage: react-native <command>

Commands:
  - start: starts the webserver
  - bundle: builds the javascript bundle for offline use
  - unbundle: builds javascript as "unbundle" for offline use
  - new-library: generates a native library bridge
  - android: generates an Android project for your app
  - run-android: builds your app and starts it on a connected Android emulator or device
  - log-android: print Android logs
  - run-ios: builds your app and starts it on iOS simulator
  - log-ios: print iOS logs
  - upgrade: upgrade your app's template files to the latest version; run this after updating the react-native version in your package.json and running npm install
  - link: link a library
'''


@pytest.mark.parametrize('command', [
    Command('react-native star', stderr=stderr('star')),
    Command('react-native android-logs', stderr=stderr('android-logs'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('gradle star', stderr=stderr('star')),
    Command('react-native start')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, result', [
    (Command('react-native star', stdout, stderr('star')),
     'react-native start'),
    (Command('react-native logsandroid -f', stdout, stderr('logsandroid')),
     'react-native log-android -f')])
def test_get_new_command(command, result):
    assert get_new_command(command)[0] == result
