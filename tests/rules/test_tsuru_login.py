import pytest
from thefuck.rules.tsuru_login import match, get_new_command
from thefuck.types import Command


error_msg = (
    "Error: you're not authenticated or your session has expired.",
    ("You're not authenticated or your session has expired. "
     "Please use \"login\" command for authentication."),
)


@pytest.mark.parametrize('command', [
    Command('tsuru app-shell', error_msg[0]),
    Command('tsuru app-log -f', error_msg[1]),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('tsuru', ''),
    Command('tsuru app-restart', 'Error: unauthorized'),
    Command('tsuru app-log -f', 'Error: unparseable data'),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('tsuru app-shell', error_msg[0]),
     'tsuru login && tsuru app-shell'),
    (Command('tsuru app-log -f', error_msg[1]),
     'tsuru login && tsuru app-log -f'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
