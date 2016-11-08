from thefuck.rules.git_flag_after_filename import match, get_new_command
from tests.utils import Command

command1 = Command('git log README.md -p',
                   stderr="fatal: bad flag '-p' used after filename")
command2 = Command('git log README.md -p CONTRIBUTING.md',
                   stderr="fatal: bad flag '-p' used after filename")
command3 = Command('git log -p README.md --name-only',
                   stderr="fatal: bad flag '--name-only' used after filename")


def test_match():
    assert match(command1)
    assert match(command2)
    assert match(command3)
    assert not match(Command('git log README.md'))
    assert not match(Command('git log -p README.md'))


def test_get_new_command():
    assert get_new_command(command1) == "git log -p README.md"
    assert get_new_command(command2) == "git log -p README.md CONTRIBUTING.md"
    assert get_new_command(command3) == "git log -p --name-only README.md"
