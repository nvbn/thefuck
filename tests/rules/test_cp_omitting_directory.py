from mock import Mock
from thefuck.rules.cp_omitting_directory import match, get_new_command


def test_match():
    assert match(Mock(script='cp dir', stderr="cp: omitting directory 'dir'"),
                 None)
    assert not match(Mock(script='some dir',
                          stderr="cp: omitting directory 'dir'"), None)
    assert not match(Mock(script='cp dir', stderr=""), None)


def test_get_new_command():
    assert get_new_command(Mock(script='cp dir'), None) == 'cp -a dir'
