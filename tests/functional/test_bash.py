import pytest
from tests.functional.utils import build_container, spawn, run, read_until, \
    root, functional

containers = [('thefuck/ubuntu-python3-bash', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN echo "PS1='$ '" > /root/.bashrc
CMD ["/bin/bash"]
'''),
              ('thefuck/ubuntu-python2-bash', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev
RUN pip2 install -U pip setuptools
RUN echo "PS1='$ '" > /root/.bashrc
CMD ["/bin/bash"]
''')]


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_with_confirmation(tag, dockerfile):
    build_container(tag, dockerfile)
    with spawn(tag, '{}:/src'.format(root),
               ['cd /src', 'pip install .', 'eval $(thefuck-alias)']) as proc:
        run(proc, 'ehco test')
        proc.sendline('fuck')
        read_until(proc, '[')
        proc.send('\n')
        out = read_until(proc)
        assert out.split('\n')[-2] == 'test\r\r'


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_without_confirmation(tag, dockerfile):
    build_container(tag, dockerfile)
    with spawn(tag, '{}:/src'.format(root),
               ['cd /src', 'pip install .',
                'export THEFUCK_REQUIRE_CONFIRMATION=false',
                'eval $(thefuck-alias)']) as proc:
        run(proc, 'ehco test')
        run(proc, 'fuck')
        out = read_until(proc)
        assert out.split('\n')[-2] == 'test\r\r'
