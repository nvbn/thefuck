import pytest
from tests.functional.utils import spawn, functional
from tests.functional.plots import with_confirmation, without_confirmation

containers = [('ubuntu-python3-zsh', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev zsh
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
CMD ["/bin/zsh"]
'''),
              ('ubuntu-python2-zsh', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev zsh
RUN pip2 install -U pip setuptools
CMD ["/bin/zsh"]
''')]


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_with_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile) as proc:
        proc.sendline('eval $(thefuck-alias)')
        with_confirmation(proc)


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_without_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile) as proc:
        proc.sendline('export THEFUCK_REQUIRE_CONFIRMATION=false')
        proc.sendline('eval $(thefuck-alias)')
        without_confirmation(proc)
