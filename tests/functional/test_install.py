import pytest
from thefuck.main import _get_current_version
from tests.functional.utils import functional


envs = ((u'bash', 'thefuck/ubuntu-bash', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy bash
'''), (u'bash', 'thefuck/generic-bash', u'''
FROM fedora:latest
RUN dnf install -yy python-devel sudo wget gcc
'''))


@functional
@pytest.mark.skip_without_docker
@pytest.mark.parametrize('shell, tag, dockerfile', envs)
def test_installation(spawnu, shell, TIMEOUT, tag, dockerfile):
    proc = spawnu(tag, dockerfile, shell)
    proc.sendline(u'cat /src/install.sh | sh - && $0')
    proc.sendline(u'thefuck --version')
    assert proc.expect([TIMEOUT, u'thefuck {}'.format(_get_current_version())],
                       timeout=600)
    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'No fucks given'])
