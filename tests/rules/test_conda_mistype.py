import pytest

from thefuck.rules.conda_mistype import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def mistype_response():
    return """

CommandNotFoundError: No command 'conda lst'.
Did you mean 'conda list'?

    """


def test_match(mistype_response):
    assert match(Command('conda lst', mistype_response))
    err_response = 'bash: codna: command not found'
    assert not match(Command('codna list', err_response))


def test_get_new_command(mistype_response):
    assert (get_new_command(Command('conda lst', mistype_response)) == ['conda list'])
