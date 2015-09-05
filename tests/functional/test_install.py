import pytest
from pexpect import TIMEOUT
from tests.functional.utils import spawn, functional, bare

envs = ((u'bash', 'ubuntu-bash', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy bash
'''), (u'bash', 'generic-bash', u'''
FROM fedora:latest
RUN dnf install -yy python-devel sudo wget gcc
'''))


@functional
@pytest.mark.skipif(
    bool(bare), reason="Can't be tested in bare run")
@pytest.mark.parametrize('shell, tag, dockerfile', envs)
def test_installation(request, shell, tag, dockerfile):
    proc = spawn(request, tag, dockerfile, shell, install=False)
    proc.sendline(u'cat /src/install.sh | sh - && $0')
    proc.sendline(u'thefuck --version')
    assert proc.expect([TIMEOUT, u'The Fuck'], timeout=600)
    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'No fucks given'])
