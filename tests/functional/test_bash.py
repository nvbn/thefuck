import pytest
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation, history_changed, history_not_changed, \
    select_command_with_arrows, how_to_configure

containers = ((u'thefuck/python3-bash',
               u'FROM python:3',
               u'bash'),
              (u'thefuck/python2-bash',
               u'FROM python:2',
               u'bash'))


@pytest.fixture(params=containers)
def proc(request, spawnu, TIMEOUT):
    proc = spawnu(*request.param)
    proc.sendline(u"pip install /src")
    assert proc.expect([TIMEOUT, u'Successfully installed'])
    proc.sendline(u"export PS1='$ '")
    proc.sendline(u'eval $(thefuck --alias)')
    proc.sendline(u'echo > $HISTFILE')
    return proc


@pytest.mark.functional
def test_with_confirmation(proc, TIMEOUT):
    with_confirmation(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, u'echo test')


@pytest.mark.functional
def test_select_command_with_arrows(proc, TIMEOUT):
    select_command_with_arrows(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, u'git help')


@pytest.mark.functional
def test_refuse_with_confirmation(proc, TIMEOUT):
    refuse_with_confirmation(proc, TIMEOUT)
    history_not_changed(proc, TIMEOUT)


@pytest.mark.functional
def test_without_confirmation(proc, TIMEOUT):
    without_confirmation(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, u'echo test')


@pytest.mark.functional
def test_how_to_configure_alias(proc, TIMEOUT):
    how_to_configure(proc, TIMEOUT)
