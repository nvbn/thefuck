import pytest
from mock import Mock
from thefuck import shells


class TestGeneric(object):
    def test_from_shell(self):
        assert shells.Generic().from_shell('pwd') == 'pwd'

    def test_to_shell(self):
        assert shells.Bash().to_shell('pwd') == 'pwd'


class TestBash(object):
    @pytest.fixture(autouse=True)
    def Popen(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr('thefuck.shells.Popen', mock)
        mock.return_value.stdout.read.return_value = (
            b'alias l=\'ls -CF\'\n'
            b'alias la=\'ls -A\'\n'
            b'alias ll=\'ls -alF\'')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after):
        assert shells.Bash().from_shell(before) == after

    def test_to_shell(self):
        assert shells.Bash().to_shell('pwd') == 'pwd'


class TestZsh(object):
    @pytest.fixture(autouse=True)
    def Popen(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr('thefuck.shells.Popen', mock)
        mock.return_value.stdout.read.return_value = (
            b'l=\'ls -CF\'\n'
            b'la=\'ls -A\'\n'
            b'll=\'ls -alF\'')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after):
        assert shells.Zsh().from_shell(before) == after

    def test_to_shell(self):
        assert shells.Zsh().to_shell('pwd') == 'pwd'