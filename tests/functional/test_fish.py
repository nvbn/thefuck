import pytest
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation
from tests.functional.utils import spawn, functional, images

containers = images(('ubuntu-python3-fish', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev fish
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
'''),
                    ('ubuntu-python2-fish', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev fish
RUN pip2 install -U pip setuptools
'''))


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_with_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile, 'fish') as proc:
        proc.sendline('thefuck-alias > ~/.config/fish/config.fish')
        proc.sendline('fish')
        with_confirmation(proc)


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_refuse_with_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile, 'fish') as proc:
        proc.sendline('thefuck-alias > ~/.config/fish/config.fish')
        proc.sendline('fish')
        refuse_with_confirmation(proc)


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_without_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile, 'fish') as proc:
        proc.sendline('thefuck-alias > ~/.config/fish/config.fish')
        proc.sendline('fish')
        without_confirmation(proc)
