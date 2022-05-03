import pytest

from thefuck.rules.git_misspelled import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize(
    "script, output",
    [
        ('''gti commit -m "this is a messsage"''', "gti: command not found"),
        ('''tgi commit -m "this is a messsage"''', "tgi: command not found"),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        ('''gti commit -m "this is a message"''', "", '''git commit -m "this is a message"'''),
        ('''tgi commit -m "this is a message"''', "", '''git commit -m "this is a message"'''),
    ],
)
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
