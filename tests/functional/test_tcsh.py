import pytest
from tests.functional.utils import spawn, functional
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation

containers = [('ubuntu-python3-tcsh', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python3 python3-pip python3-dev tcsh
RUN pip3 install -U setuptools
RUN ln -s /usr/bin/pip3 /usr/bin/pip
CMD ["/usr/bin/tcsh"]
'''),
              ('ubuntu-python2-tcsh', '''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy python python-pip python-dev tcsh
RUN pip2 install -U pip setuptools
CMD ["/usr/bin/tcsh"]
''')]


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_with_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile) as proc:
        proc.sendline('tcsh')
        proc.sendline('eval `thefuck-alias`')
        with_confirmation(proc)


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_refuse_with_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile) as proc:
        proc.sendline('tcsh')
        proc.sendline('eval `thefuck-alias`')
        refuse_with_confirmation(proc)


@functional
@pytest.mark.parametrize('tag, dockerfile', containers)
def test_without_confirmation(tag, dockerfile):
    with spawn(tag, dockerfile) as proc:
        proc.sendline('tcsh')
        proc.sendline('mkdir ~/.thefuck')
        proc.sendline('echo "require_confirmation = False" >> ~/.thefuck/settings.py')
        proc.sendline('eval `thefuck-alias`')
        without_confirmation(proc)
