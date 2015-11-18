from thefuck.rules.systemctl import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('systemctl nginx start', stderr='Unknown operation \'nginx\'.'))
    assert match(Command('sudo systemctl nginx start', stderr='Unknown operation \'nginx\'.'))
    assert not match(Command('systemctl start nginx'))
    assert not match(Command('systemctl start nginx'))
    assert not match(Command('sudo systemctl nginx', stderr='Unknown operation \'nginx\'.'))
    assert not match(Command('systemctl nginx', stderr='Unknown operation \'nginx\'.'))
    assert not match(Command('systemctl start wtf', stderr='Failed to start wtf.service: Unit wtf.service failed to load: No such file or directory.'))


def test_get_new_command():
    assert get_new_command(Command('systemctl nginx start')) == "systemctl start nginx"
    assert get_new_command(Command('sudo systemctl nginx start')) == "sudo systemctl start nginx"
