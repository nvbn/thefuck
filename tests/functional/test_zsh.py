import pytest
from tests.functional.utils import build_container, spawn, run, read_until, \
    root, functional

containers = [('thefuck/ubuntu-python3-zsh', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev zsh
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN echo "PS1='\\n$ '" > /root/.zshrc
CMD ["/bin/zsh"]
'''),
              ('thefuck/ubuntu-python2-zsh', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev zsh
RUN pip2 install -U pip setuptools
RUN echo "PS1='\\n$ '" > /root/.zshrc
CMD ["/bin/zsh"]
''')]


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_with_confirmation(tag, dockerfile):
    build_container(tag, dockerfile)
    with spawn(tag, '{}:/src'.format(root),
               ['cd /src', 'pip install .', 'eval $(thefuck-alias)']) as proc:
        run(proc, 'ehco "\ntest"')
        proc.sendline('fuck')
        read_until(proc, '[')
        proc.send('\n')
        read_until(proc)
        out = read_until(proc)
        assert out.split('\n')[-3] == 'test\r\r'


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_without_confirmation(tag, dockerfile):
    build_container(tag, dockerfile)
    with spawn(tag, '{}:/src'.format(root),
               ['cd /src', 'pip install .',
                'export THEFUCK_REQUIRE_CONFIRMATION=false',
                'eval $(thefuck-alias)']) as proc:
        run(proc, 'ehco "\ntest"')
        run(proc, 'fuck')
        out = read_until(proc)
        assert out.split('\n')[-3] == 'test\r\r'
