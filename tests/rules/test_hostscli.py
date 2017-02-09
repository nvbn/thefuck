import pytest
from thefuck.rules.hostscli import no_command, no_website, get_new_command, \
    match
from tests.utils import Command


no_command = '''
Usage: hostscli [OPTIONS] COMMAND [ARGS]...

%s "invalid".
''' % no_command


no_website = '''
%s:

No Domain list found for website: a_website_that_does_not_exist

Please raise a Issue here: https://github.com/dhilipsiva/hostscli/issues/new
if you think we should add domains for this website.

type `hostscli websites` to see a list of websites that you can block/unblock
''' % no_website


@pytest.mark.parametrize('command', [
    Command('hostscli invalid', stderr=no_command)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, result', [
    (Command(
        'hostscli invalid', stderr=no_command), ['hostscli --help']),
    (Command(
        'sudo hostscli block a_website_that_does_not_exist',
        stderr=no_website),
     ['hostscli websites'])])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
