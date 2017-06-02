import pytest
from thefuck.rules import dnf_install
from tests.utils import Command


@pytest.mark.parametrize('command, new_command', [
    (Command('dfn install python'), 'sudo dnf install python'),
    (Command('dnf istall python'), 'sudo dnf install python'),
    (Command('dfn install python'), 'sudo dnf install python'),
    (Command('dfn install python ruby'), 'sudo dnf install python ruby')])
def test_get_new_command(command, new_command):
    assert dnf_install.get_new_command(command) == new_command
