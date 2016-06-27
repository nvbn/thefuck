import pytest
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation, history_changed, history_not_changed, \
    select_command_with_arrows, how_to_configure

containers = (('thefuck/ubuntu-python3-zsh',
               u'''FROM ubuntu:latest
                   RUN apt-get update
                   RUN apt-get install -yy python3 python3-pip python3-dev git
                   RUN pip3 install -U setuptools
                   RUN ln -s /usr/bin/pip3 /usr/bin/pip
                   RUN apt-get install -yy zsh''',
               u'zsh'),
              ('thefuck/ubuntu-python2-zsh',
               u'''FROM ubuntu:latest
                   RUN apt-get update
                   RUN apt-get install -yy python python-pip python-dev git
                   RUN pip2 install -U pip setuptools
                   RUN apt-get install -yy zsh''',
               u'zsh'))


@pytest.fixture(params=containers)
def proc(request, spawnu, run_without_docker):
    proc = spawnu(*request.param)
    if not run_without_docker:
        proc.sendline(u'pip install /src')
    proc.sendline(u'eval $(thefuck --alias)')
    proc.sendline(u'export HISTFILE=~/.zsh_history')
    proc.sendline(u'echo > $HISTFILE')
    proc.sendline(u'export SAVEHIST=100')
    proc.sendline(u'export HISTSIZE=100')
    proc.sendline(u'setopt INC_APPEND_HISTORY')
    return proc


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_with_confirmation(proc, TIMEOUT):
    with_confirmation(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, u'echo test')


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_select_command_with_arrows(proc, TIMEOUT):
    select_command_with_arrows(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, u'git help')


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_refuse_with_confirmation(proc, TIMEOUT):
    refuse_with_confirmation(proc, TIMEOUT)
    history_not_changed(proc, TIMEOUT)


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_without_confirmation(proc, TIMEOUT):
    without_confirmation(proc, TIMEOUT)
    history_changed(proc, TIMEOUT, u'echo test')


@pytest.mark.functional
@pytest.mark.once_without_docker
def test_how_to_configure_alias(proc, TIMEOUT):
    how_to_configure(proc, TIMEOUT)
