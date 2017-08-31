import pytest

from thefuck.types import Command
from thefuck.rules.tsuru_not_command import match, get_new_command


@pytest.mark.parametrize('command', [
    Command('tsuru log', (
        'tsuru: "tchururu" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
        '\tapp-log\n'
        '\tlogin\n'
        '\tlogout\n'
    )),
    Command('tsuru app-l', (
        'tsuru: "tchururu" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
        '\tapp-list\n'
        '\tapp-log\n'
    )),
    Command('tsuru user-list', (
        'tsuru: "tchururu" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
        '\tteam-user-list\n'
    )),
    Command('tsuru targetlist', (
        'tsuru: "tchururu" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
        '\ttarget-list\n'
    )),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('tsuru tchururu', (
        'tsuru: "tchururu" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
    )),
    Command('tsuru version', 'tsuru version 0.16.0.'),
    Command('tsuru help', (
        'tsuru version 0.16.0.\n'
        '\nUsage: tsuru command [args]\n'
    )),
    Command('tsuru platform-list', (
        '- java\n'
        '- logstashgiro\n'
        '- newnode\n'
        '- nodejs\n'
        '- php\n'
        '- python\n'
        '- python3\n'
        '- ruby\n'
        '- ruby20\n'
        '- static\n'
    )),
    Command('tsuru env-get', 'Error: App thefuck not found.'),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_commands', [
    (Command('tsuru log', (
        'tsuru: "log" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
        '\tapp-log\n'
        '\tlogin\n'
        '\tlogout\n'
    )), ['tsuru login', 'tsuru logout', 'tsuru app-log']),
    (Command('tsuru app-l', (
        'tsuru: "app-l" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
        '\tapp-list\n'
        '\tapp-log\n'
    )), ['tsuru app-log', 'tsuru app-list']),
    (Command('tsuru user-list', (
        'tsuru: "user-list" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
        '\tteam-user-list\n'
    )), ['tsuru team-user-list']),
    (Command('tsuru targetlist', (
        'tsuru: "targetlist" is not a tsuru command. See "tsuru help".\n'
        '\nDid you mean?\n'
        '\ttarget-list\n'
    )), ['tsuru target-list']),
])
def test_get_new_command(command, new_commands):
    assert get_new_command(command) == new_commands
