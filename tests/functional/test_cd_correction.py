import pytest

dockerfile = u'''
FROM python:3
RUN adduser --disabled-password --gecos '' test
WORKDIR /src
USER test
RUN echo 'eval $(thefuck --alias)' > /home/test/.bashrc
RUN echo > /home/test/.bash_history
RUN mkdir -p /home/test/some/random/folder
RUN mkdir -p /home/test/another/random/folder
USER root
'''


def plot(proc, TIMEOUT):
    proc.sendline(u'cd /home/test/some/random')
    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'No fucks given'])
    proc.sendline(u'cd flder')
    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'cd "/home/test/some/random/folder"'])
    proc.send('\n')
    proc.sendline(u'pwd')
    assert proc.expect([TIMEOUT, u'/home/test/some/random/folder'])
    proc.sendline(u'cd /home/test/another/randm/folder/')
    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'cd "/home/test/another/random/folder"'])
    proc.send('\n')
    proc.sendline(u'pwd')
    assert proc.expect([TIMEOUT, u'/home/test/another/random/folder'])


@pytest.mark.functional
def test_performance(spawnu, TIMEOUT, benchmark):
    proc = spawnu(u'thefuck/python3-cd_correction-functional',
                  dockerfile, u'bash')
    proc.sendline(u'pip install /src')
    proc.sendline(u'su test')
    assert benchmark(plot, proc, TIMEOUT) is None
