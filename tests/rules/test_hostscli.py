import pytest
from thefuck.rules.hostscli import no_website, get_new_command, match
from thefuck.types import Command

no_website_long = '''
{}:

No Domain list found for website: a_website_that_does_not_exist

Please raise a Issue here: https://github.com/dhilipsiva/hostscli/issues/new
if you think we should add domains for this website.

type `hostscli websites` to see a list of websites that you can block/unblock
'''.format(no_website)


@pytest.mark.parametrize('command', [
    Command('hostscli block a_website_that_does_not_exist', no_website_long)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, result', [(
    Command('hostscli block a_website_that_does_not_exist', no_website_long),
    ['hostscli websites'])])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
