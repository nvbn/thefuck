import pytest
from thefuck.rules.tsuru_login import match, get_new_command
from tests.utils import Command


error_msg = (
    "Error: you're not authenticated or your session has expired.",
    ("You're not authenticated or your session has expired. "
     "Please use \"login\" command for authentication."),
)


@pytest.mark.parametrize('command', [
    Command(script='tsuru app-shell', stderr=error_msg[0]),
    Command(script='tsuru app-log -f', stderr=error_msg[1]),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='tsuru'),
    Command(script='tsuru app-restart', stderr=('Error: unauthorized')),
    Command(script='tsuru app-log -f', stderr=('Error: unparseable data')),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('tsuru app-shell', stderr=error_msg[0]),
     'tsuru login && tsuru app-shell'),
    (Command('tsuru app-log -f', stderr=error_msg[1]),
     'tsuru login && tsuru app-log -f'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
