import pytest
from tests.functional.utils import spawn, functional, images
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation

containers = images(('ubuntu-python3-tcsh', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev tcsh
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
'''),
                    ('ubuntu-python2-tcsh', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev tcsh
RUN pip2 install -U pip setuptools
'''))


@pytest.fixture(params=containers)
def proc(request):
    tag, dockerfile = request.param
    proc = spawn(request, tag, dockerfile, u'tcsh')
    proc.sendline(u'tcsh')
    proc.sendline(u'eval `thefuck-alias`')
    return proc


@functional
def test_with_confirmation(proc):
    with_confirmation(proc)


@functional
def test_refuse_with_confirmation(proc):
    refuse_with_confirmation(proc)


@functional
def test_without_confirmation(proc):
    without_confirmation(proc)

# TODO: ensure that history changes.
