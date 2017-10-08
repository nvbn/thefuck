import pytest
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation, history_changed, history_not_changed, \
    select_command_with_arrows, how_to_configure


python_3 = (u'thefuck/python3-bash',
            u'FROM python:3',
            u'sh')

python_2 = (u'thefuck/python2-bash',
            u'FROM python:2',
            u'sh')


init_bashrc = u'''echo '
export SHELL=/bin/bash
export PS1="$ "
echo > $HISTFILE
eval $(thefuck --alias {})
echo "instant mode ready: $THEFUCK_INSTANT_MODE"
' > ~/.bashrc'''


@pytest.fixture(params=[(python_3, False),
                        (python_3, True),
                        (python_2, False)])
def proc(request, spawnu, TIMEOUT):
    container, instant_mode = request.param
    proc = spawnu(*container)
    proc.sendline(u"pip install /src")
    assert proc.expect([TIMEOUT, u'Successfully installed'])
    proc.sendline(init_bashrc.format(
        u'--enable-experimental-instant-mode' if instant_mode else ''))
    proc.sendline(u"bash")
    if instant_mode:
        assert proc.expect([TIMEOUT, u'instant mode ready: True'])
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
    proc.sendline('unset -f fuck')
    how_to_configure(proc, TIMEOUT)
