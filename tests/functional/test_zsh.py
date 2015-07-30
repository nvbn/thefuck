import pytest
from tests.functional.utils import spawn, functional, images
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation, history_changed, history_not_changed, select_command_with_arrows

containers = images(('ubuntu-python3-zsh', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev git
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN apt-get install -yy zsh
'''),
                    ('ubuntu-python2-zsh', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev git
RUN pip2 install -U pip setuptools
RUN apt-get install -yy zsh
'''))


@pytest.fixture(params=containers)
def proc(request):
    tag, dockerfile = request.param
    proc = spawn(request, tag, dockerfile, u'zsh')
    proc.sendline(u'eval $(thefuck-alias)')
    proc.sendline(u'export HISTFILE=~/.zsh_history')
    proc.sendline(u'touch $HISTFILE')
    return proc


@functional
def test_with_confirmation(proc):
    with_confirmation(proc)
    history_changed(proc, u'echo test')


@functional
def test_select_command_with_arrows(proc):
    select_command_with_arrows(proc)
    history_changed(proc, u'git push')


@functional
def test_refuse_with_confirmation(proc):
    refuse_with_confirmation(proc)
    history_not_changed(proc)


@functional
def test_without_confirmation(proc):
    without_confirmation(proc)
    history_changed(proc, u'echo test')
