import pytest
from thefuck.rules.quotation_marks import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script="git commit -m \'My Message\""),
    Command(script="git commit -am \"Mismatched Quotation Marks\'"),
    Command(script="echo \"hello\'")])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command("git commit -m \'My Message\""), "git commit -m \"My Message\""),
    (Command("git commit -am \"Mismatched Quotation Marks\'"), "git commit -am \"Mismatched Quotation Marks\""),
    (Command("echo \"hello\'"), "echo \"hello\"")])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
