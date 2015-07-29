import pytest
from mock import Mock
from thefuck.rules.lein_not_task import match, get_new_command


@pytest.fixture
def is_not_task():
    return ''''rpl' is not a task. See 'lein help'.

Did you mean this?
         repl
         jar
'''


def test_match(is_not_task):
    assert match(Mock(script='lein rpl', stderr=is_not_task), None)
    assert not match(Mock(script='ls', stderr=is_not_task), None)


def test_get_new_command(is_not_task):
    assert get_new_command(Mock(script='lein rpl --help', stderr=is_not_task),
                           None) == ['lein repl --help', 'lein jar --help']
