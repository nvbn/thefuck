from thefuck.rules.go_unknown_command import match
from thefuck.types import Command

_GO_BUILD_MISSPELLED_OUTPUT = """go bulid: unknown command
Run 'go help' for usage."""


def test_match():
    assert match(Command('go bulid', _GO_BUILD_MISSPELLED_OUTPUT))


def test_not_match():
    assert not match(Command('go run', 'go run: no go files listed'))
