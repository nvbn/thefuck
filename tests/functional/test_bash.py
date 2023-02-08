import pytest

from tests.functional.plots import (history_changed, history_not_changed, how_to_configure, refuse_with_confirmation,
                                    select_command_with_arrows, with_confirmation, without_confirmation)

python_3 = ('thefuck/python3-bash',
            'FROM python:3',
            'sh')

python_2 = ('thefuck/python2-bash',
            'FROM python:2',
            'sh')


init_bashrc = '''echo '
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
    proc.sendline("pip install /src")
    assert proc.expect([TIMEOUT, 'Successfully installed'])
    proc.sendline(init_bashrc.format(
        '--enable-experimental-instant-mode' if instant_mode else ''))
    proc.sendline("bash")
    if instant_mode:
        assert proc.expect([TIMEOUT, 'instant mode ready: True'])
    return proc


@pytest.mark.functional
def test_with_confirmation(proc, TIMEOUT):
    with_confirmation(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, 'echo test')


@pytest.mark.functional
def test_select_command_with_arrows(proc, TIMEOUT):
    select_command_with_arrows(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, 'git help')


@pytest.mark.functional
def test_refuse_with_confirmation(proc, TIMEOUT):
    refuse_with_confirmation(proc, TIMEOUT)
    history_not_changed(proc, TIMEOUT)


@pytest.mark.functional
def test_without_confirmation(proc, TIMEOUT):
    without_confirmation(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, 'echo test')


@pytest.mark.functional
def test_how_to_configure_alias(proc, TIMEOUT):
    proc.sendline('unset -f fuck')
    how_to_configure(proc, TIMEOUT)
