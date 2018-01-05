import pytest
from thefuck.rules.adb_unknown_command import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return '''Android Debug Bridge version 1.0.31

 -d                            - directs command to the only connected USB device
                                 returns an error if more than one USB device is present.
 -e                            - directs command to the only running emulator.
                                 returns an error if more than one emulator is running.
 -s <specific device>          - directs command to the device or emulator with the given
                                 serial number or qualifier. Overrides ANDROID_SERIAL
                                 environment variable.
'''


@pytest.mark.parametrize('script', [
    ('adb lgcat'),
    ('adb puhs')])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', [
    'git branch foo',
    'abd push'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, new_command', [
    ('adb puhs test.bin /sdcard/test.bin', 'adb push test.bin /sdcard/test.bin'),
    ('adb -s 1111 logcta', 'adb -s 1111 logcat'),
    ('adb -P 666 pulll /sdcard/test.bin', 'adb -P 666 pull /sdcard/test.bin'),
    ('adb -d logcatt', 'adb -d logcat'),
    ('adb -e reboott', 'adb -e reboot')])
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
