import pytest
import time

dockerfile = u'''
FROM python:3
RUN adduser --disabled-password --gecos '' test
ENV SEED "{seed}"
WORKDIR /src
USER test
RUN echo 'eval $(thefuck --alias)' > /home/test/.bashrc
RUN echo > /home/test/.bash_history
RUN git config --global user.email "you@example.com"
RUN git config --global user.name "Your Name"
USER root
'''.format(seed=time.time())


def plot(proc, TIMEOUT):
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


@pytest.mark.functional
@pytest.mark.benchmark(min_rounds=10)
def test_performance(spawnu, TIMEOUT, benchmark):
    proc = spawnu(u'thefuck/python3-bash-performance',
                  dockerfile, u'bash')
    proc.sendline(u'pip install /src')
    proc.sendline(u'su test')
    assert benchmark(plot, proc, TIMEOUT) is None
