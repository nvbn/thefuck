import pytest
from thefuck.rules.git_help_aliased import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('script, output', [
    ('git help st', "`git st' is aliased to `status'"),
    ('git help ds', "`git ds' is aliased to `diff --staged'")])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('git help status', "GIT-STATUS(1)...Git Manual...GIT-STATUS(1)"),
    ('git help diff', "GIT-DIFF(1)...Git Manual...GIT-DIFF(1)")])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('script, output, new_command', [
    ('git help st', "`git st' is aliased to `status'", 'git help status'),
    ('git help ds', "`git ds' is aliased to `diff --staged'", 'git help diff')])
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
