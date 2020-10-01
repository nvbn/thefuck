import pytest
from thefuck.rules.composer_not_command import match, get_new_command
from thefuck.types import Command


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


@pytest.fixture
def composer_require_instead_of_install():
    return 'Invalid argument package. Use "composer require package" instead to add packages to your composer.json.'


def test_match(composer_not_command, composer_not_command_one_of_this, composer_require_instead_of_install):
    assert match(Command('composer udpate',
                         composer_not_command))
    assert match(Command('composer pdate',
                         composer_not_command_one_of_this))
    assert match(Command('composer install package',
                         composer_require_instead_of_install))
    assert not match(Command('ls update', composer_not_command))


def test_get_new_command(composer_not_command, composer_not_command_one_of_this, composer_require_instead_of_install):
    assert (get_new_command(Command('composer udpate',
                                    composer_not_command))
            == 'composer update')
    assert (get_new_command(Command('composer pdate',
                                    composer_not_command_one_of_this))
            == 'composer selfupdate')
    assert (get_new_command(Command('composer install package',
                                    composer_require_instead_of_install))
            == 'composer require package')
