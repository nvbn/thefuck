import pytest
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation, select_command_with_arrows
from tests.functional.utils import spawn, functional, images, bare

containers = images(('ubuntu-python3-fish', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev fish git
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN apt-get install -yy fish
'''),
                    ('ubuntu-python2-fish', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev git
RUN pip2 install -U pip setuptools
RUN apt-get install -yy fish
'''))


@pytest.fixture(params=containers)
def proc(request):
    tag, dockerfile = request.param
    proc = spawn(request, tag, dockerfile, u'fish')
    proc.sendline(u'thefuck-alias > ~/.config/fish/config.fish')
    proc.sendline(u'fish')
    return proc


@functional
@pytest.mark.skipif(
    bool(bare), reason='https://github.com/travis-ci/apt-source-whitelist/issues/71')
def test_with_confirmation(proc):
    with_confirmation(proc)


@functional
def test_select_command_with_arrows(proc):
    select_command_with_arrows(proc)


@functional
@pytest.mark.skipif(
    bool(bare), reason='https://github.com/travis-ci/apt-source-whitelist/issues/71')
def test_refuse_with_confirmation(proc):
    refuse_with_confirmation(proc)


@functional
@pytest.mark.skipif(
    bool(bare), reason='https://github.com/travis-ci/apt-source-whitelist/issues/71')
def test_without_confirmation(proc):
    without_confirmation(proc)

# TODO: ensure that history changes.
