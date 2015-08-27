import pytest
from thefuck.rules.lein_not_task import match, get_new_command
from tests.utils import Command


@pytest.fixture
def is_not_task():
    return ''''rpl' is not a task. See 'lein help'.

Did you mean this?
         repl
         jar
'''


def test_match(is_not_task):
    assert match(Command(script='lein rpl', stderr=is_not_task), None)
    assert not match(Command(script='ls', stderr=is_not_task), None)


def test_get_new_command(is_not_task):
    assert get_new_command(Command(script='lein rpl --help', stderr=is_not_task),
                           None) == ['lein repl --help', 'lein jar --help']
