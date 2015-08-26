from pexpect import TIMEOUT
import pytest
import time
from tests.functional.utils import spawn, functional, bare

dockerfile = u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev git
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN adduser --disabled-password --gecos '' test
ENV SEED "{seed}"
COPY thefuck /src
WORKDIR /src
RUN pip install .
USER test
RUN echo 'eval $(thefuck --alias)' > /home/test/.bashrc
RUN echo > /home/test/.bash_history
RUN git config --global user.email "you@example.com"
RUN git config --global user.name "Your Name"
'''.format(seed=time.time())


@pytest.fixture
def proc(request):
    return spawn(request, 'ubuntu-python3-bash-performance',
                 dockerfile, u'bash', install=False, copy_src=True)


def plot(proc):
    proc.sendline(u'cd /home/test/')
    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'No fucks given'])
    proc.sendline(u'git init')
    proc.sendline(u'git add .')
    proc.sendline(u'git commit -a -m init')
    proc.sendline(u'git brnch')
    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'git branch'])
    proc.send('\n')
    assert proc.expect([TIMEOUT, u'master'])
    proc.sendline(u'echo test')
    proc.sendline(u'echo tst')
    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'echo test'])
    proc.send('\n')
    assert proc.expect([TIMEOUT, u'test'])


@functional
@pytest.mark.skipif(
    bool(bare), reason='Would lie on a bare run')
@pytest.mark.benchmark(min_rounds=10)
def test_performance(proc, benchmark):
    assert benchmark(plot, proc) is None
