import pytest
from thefuck.rules.rvm_not_installed import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return ('Required ruby-2.7.2 is not installed.\n'
            'To install do: \'rvm install "ruby-2.7.2"\'')


@pytest.fixture
def output_v3():
    return ('Required ruby-3.0.0 is not installed.\n'
            'To install do: \'rvm install "ruby-3.0.0"\'')


def test_match(output):
    assert match(Command('rvm use 2.7.2', output))


def test_match_v3(output_v3):
    assert match(Command('rvm use 3.0.0', output_v3))


def test_not_match():
    assert not match(Command('rvm list', ''))
    assert not match(Command('rvm use 2.7.2', 'Using ruby-2.7.2'))
    assert not match(Command('echo hello', 'hello'))
    # Should not match other tools
    assert not match(Command('gem install rails',
                             'Required ruby-2.7.2 is not installed.\n'
                             'To install do: \'rvm install "ruby-2.7.2"\''))


def test_get_new_command(output):
    assert get_new_command(Command('rvm use 2.7.2', output)) == 'rvm install ruby-2.7.2'


def test_get_new_command_v3(output_v3):
    assert get_new_command(Command('rvm use 3.0.0', output_v3)) == 'rvm install ruby-3.0.0'
