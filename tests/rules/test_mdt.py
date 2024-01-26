import pytest
from thefuck.rules.mdt import match, get_new_command
from thefuck.types import Command

output_unknown_shell = """Unknown command 'shll': try 'mdt help'"""

output_unknown_devices = """Unknown command 'dvices': try 'mdt help'"""

output_unknown_reboot = """Unknown command 'rboot': try 'mdt help'"""

output_unknown_version = """Unknown command 'verson': try 'mdt help'"""

output_unknown_wait = """Unknown command 'wai-for-dvice': try 'mdt help'"""


@pytest.mark.parametrize('command', [
    Command('mdt shll', output_unknown_shell),
    Command('mdt dvices', output_unknown_devices),
    Command('mdt rboot', output_unknown_reboot),
    Command('mdt verson', output_unknown_version),
    Command('mdt wai-for-dvice', output_unknown_wait)
])
def test_match(command):
    # check mdt detection
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('mdt shll', output_unknown_shell), 'mdt shell'),
    (Command('mdt dvices', output_unknown_devices), 'mdt devices'),
    (Command('mdt rboot', output_unknown_reboot), 'mdt reboot'),
    (Command('mdt verson', output_unknown_version), 'mdt version'),
    (Command('mdt wai-for-dvice', output_unknown_wait), 'mdt wait-for-device')
])
def test_get_new_command(command, new_command):
    # check first correction
    assert get_new_command(command)[0] == new_command
