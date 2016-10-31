from thefuck.rules.git_flag_after_filename import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('git log README.md -p', stderr="fatal: bad flag '-p' used after filename"))
    assert match(Command('git log README.md -p CONTRIBUTING.md', stderr="fatal: bad flag '-p' used after filename"))
    assert match(Command('git log -p README.md --name-only', stderr="fatal: bad flag '--name-only' used after filename"))
    assert not match(Command('git log README.md'))
    assert not match(Command('git log -p README.md'))


def test_get_new_command():
    assert get_new_command(Command('git log README.md -p', stderr="fatal: bad flag '-p' used after filename"))\
        == "git log -p README.md"
    assert get_new_command(Command('git log README.md -p CONTRIBUTING.md', stderr="fatal: bad flag '-p' used after filename"))\
        == "git log -p README.md CONTRIBUTING.md"
    assert get_new_command(Command('git log -p README.md --name-only', stderr="fatal: bad flag '--name-only' used after filename"))\
        == "git log -p --name-only README.md"
