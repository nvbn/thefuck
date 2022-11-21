import textwrap
from collections import namedtuple

import pytest

from thefuck.types import Command
from thefuck.rules.kedro_no_such_command import match, get_new_command

USAGE_ERROR_MESSAGE = """\
Usage: kedro [OPTIONS] COMMAND [ARGS]...
Try 'kedro -h' for help.

Error: No such command '{broken_cmd}'.
"""

CommandSuggestions = namedtuple(
    'CommandSuggestions', ['broken_cmd', 'new_cmds', 'args'], defaults=([],)
)


@pytest.fixture
def command(request):
    script = ' '.join(['kedro', request.param.broken_cmd, *request.param.args])
    output = USAGE_ERROR_MESSAGE.format(broken_cmd=request.param.broken_cmd)

    if not request.param.new_cmds:
        return Command(script, output)

    if len(request.param.new_cmds) == 1:
        suggestion = '\n\nDid you mean this?'
    else:
        suggestion = '\n\nDid you mean one of these?\n'
    suggestion += textwrap.indent('\n'.join(request.param.new_cmds), ' ' * 4)
    return Command(script, output + suggestion)


@pytest.mark.parametrize('command', [
    CommandSuggestions('ne', ['new'], ['--starter', 'spaceflights']),
    CommandSuggestions('build', ['build-reqs', 'build-docs']),
    CommandSuggestions('lin', ['lint', 'info', 'pipeline']),
    CommandSuggestions('pipline', ['pipeline', 'lint'], ['create', 'data_processing']),
], indirect=True)
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    CommandSuggestions('create', []),
], indirect=True)
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, result', [
    (CommandSuggestions('ne', ['new'], ['--starter', 'spaceflights']),
     ['kedro new --starter spaceflights']),
    (CommandSuggestions('build', ['build-reqs', 'build-docs']),
     ['kedro build-reqs', 'kedro build-docs']),
    (CommandSuggestions('lin', ['lint', 'info', 'pipeline']),
     ['kedro lint', 'kedro info', 'kedro pipeline']),
    (CommandSuggestions('pipline', ['pipeline', 'lint'], ['create', 'data_processing']),
     ['kedro pipeline create data_processing', 'kedro lint create data_processing']),
], indirect=['command'])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
