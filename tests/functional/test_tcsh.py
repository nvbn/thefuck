import pytest

from tests.functional.plots import (refuse_with_confirmation, select_command_with_arrows, with_confirmation,
                                    without_confirmation)

containers = (('thefuck/python3-tcsh',
               '''FROM python:3
                   RUN apt-get update
                   RUN apt-get install -yy tcsh''',
               'tcsh'),
              ('thefuck/python2-tcsh',
               '''FROM python:2
                   RUN apt-get update
                   RUN apt-get install -yy tcsh''',
               'tcsh'))


@pytest.fixture(params=containers)
def proc(request, spawnu, TIMEOUT):
    proc = spawnu(*request.param)
    proc.sendline('pip install /src')
    assert proc.expect([TIMEOUT, 'Successfully installed'])
    proc.sendline('tcsh')
    proc.sendline('setenv PYTHONIOENCODING utf8')
    proc.sendline('eval `thefuck --alias`')
    return proc


@pytest.mark.functional
def test_with_confirmation(proc, TIMEOUT):
    with_confirmation(proc, TIMEOUT)


@pytest.mark.functional
def test_select_command_with_arrows(proc, TIMEOUT):
    select_command_with_arrows(proc, TIMEOUT)


@pytest.mark.functional
def test_refuse_with_confirmation(proc, TIMEOUT):
    refuse_with_confirmation(proc, TIMEOUT)


@pytest.mark.functional
def test_without_confirmation(proc, TIMEOUT):
    without_confirmation(proc, TIMEOUT)

# TODO: ensure that history changes.
