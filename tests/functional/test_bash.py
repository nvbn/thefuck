import pytest
from tests.functional.utils import spawn, functional

containers = [('thefuck/ubuntu-python3-bash', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
CMD ["/bin/bash"]
'''),
              ('thefuck/ubuntu-python2-bash', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev
RUN pip2 install -U pip setuptools
CMD ["/bin/bash"]
''')]


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_with_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile) as proc:
        proc.sendline('eval $(thefuck-alias)')

        proc.sendline('ehco test')
        proc.expect('command not found')

        proc.sendline('fuck')
        proc.expect('echo test')
        proc.expect('enter')
        proc.expect_exact('ctrl+c')
        proc.send('\n')

        proc.expect('test')


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_without_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile) as proc:
        proc.sendline('export THEFUCK_REQUIRE_CONFIRMATION=false')
        proc.sendline('eval $(thefuck-alias)')

        proc.sendline('ehco test')
        proc.expect('command not found')

        proc.sendline('fuck')
        proc.expect('echo test')
        proc.expect('test')
