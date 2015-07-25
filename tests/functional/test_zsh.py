import pytest
from tests.functional.utils import spawn, functional, images
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation

containers = images(('ubuntu-python3-zsh', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev zsh
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
'''),
                    ('ubuntu-python2-zsh', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev zsh
RUN pip2 install -U pip setuptools
'''))


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_with_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile, u'zsh') as proc:
        proc.sendline(u'eval $(thefuck-alias)')
        with_confirmation(proc)


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_refuse_with_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile, u'zsh') as proc:
        proc.sendline(u'eval $(thefuck-alias)')
        refuse_with_confirmation(proc)


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_without_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile, u'zsh') as proc:
        proc.sendline(u'eval $(thefuck-alias)')
        without_confirmation(proc)
