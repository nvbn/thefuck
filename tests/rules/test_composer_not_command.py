import pytest
from thefuck.rules.composer_not_command import match, get_new_command
from tests.utils import Command


@pytest.fixture
def composer_not_command():
    # that weird spacing is part of the actual command output
    return (
        '\n'
        '\n'
        '                                    \n'
        '  [InvalidArgumentException]        \n'
        '  Command "udpate" is not defined.  \n'
        '  Did you mean this?                \n'
        '      update                        \n'
        '                                    \n'
        '\n'
        '\n'
    )


@pytest.fixture
def composer_not_command_one_of_this():
    # that weird spacing is part of the actual command output
    return (
        '\n'
        '\n'
        '                                   \n'
        '  [InvalidArgumentException]       \n'
        '  Command "pdate" is not defined.  \n'
        '  Did you mean one of these?       \n'
        '      selfupdate                   \n'
        '      self-update                  \n'
        '      update                       \n'
        '                                   \n'
        '\n'
        '\n'
    )


def test_match(composer_not_command, composer_not_command_one_of_this):
    assert match(Command('composer udpate',
                         stderr=composer_not_command))
    assert match(Command('composer pdate',
                         stderr=composer_not_command_one_of_this))
    assert not match(Command('ls update', stderr=composer_not_command))


def test_get_new_command(composer_not_command, composer_not_command_one_of_this):
    assert get_new_command(Command('composer udpate',
                                   stderr=composer_not_command)) \
           == 'composer update'
    assert get_new_command(
        Command('composer pdate', stderr=composer_not_command_one_of_this)) \
           == 'composer selfupdate'
