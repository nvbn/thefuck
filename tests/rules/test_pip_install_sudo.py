import pytest
from thefuck.rules.pip_install_sudo import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stdout_success():
    return '''
    Collecting thefuck
      Downloading thefuck-1.30.tar.gz
    Requirement already satisfied (use --upgrade to upgrade): pathlib in /usr/local/lib/python2.7/site-packages/pathlib-1.0.1-py2.7.egg (from thefuck)
    Requirement already satisfied (use --upgrade to upgrade): psutil in /usr/local/lib/python2.7/site-packages/psutil-2.2.1-py2.7-macosx-10.10-x86_64.egg (from thefuck)
    Requirement already satisfied (use --upgrade to upgrade): colorama in /usr/local/lib/python2.7/site-packages/colorama-0.3.3-py2.7.egg (from thefuck)
    Requirement already satisfied (use --upgrade to upgrade): six in /usr/local/lib/python2.7/site-packages (from thefuck)
    Installing collected packages: thefuck
      Running setup.py install for thefuck
    Successfully installed thefuck-1.30
    '''


@pytest.fixture
def stdout():
    return '''
    Collecting ipaddr
      Using cached ipaddr-2.1.11.tar.gz
    Installing collected packages: ipaddr
      Running setup.py install for ipaddr
        Complete output from command /usr/bin/python -c "import setuptools, tokenize;__file__='/tmp/pip-build-usOyBh/ipaddr/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /tmp/pip-ghPfAW-record/install-record.txt --single-version-externally-managed --compile:
        running install
        running build
        running build_py
        creating build
        creating build/lib.linux-x86_64-2.7
        copying ipaddr.py -> build/lib.linux-x86_64-2.7
        running install_lib
        copying build/lib.linux-x86_64-2.7/ipaddr.py -> /usr/local/lib/python2.7/dist-packages
        error: [Errno 13] Permission denied: '/usr/local/lib/python2.7/dist-packages/ipaddr.py'
    '''


@pytest.fixture
def stderr():
    return '''
    Command "/usr/bin/python -c "import setuptools, tokenize;__file__='/tmp/pip-build-usOyBh/ipaddr/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /tmp/pip-ghPfAW-record/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-build-usOyBh/ipaddr
    '''


def test_match(stdout, stdout_success, stderr):
    assert match(Command('pip install ipaddr', stdout=stdout, stderr=stderr),
                 None)
    assert not match(Command('pip install thefuck', stdout=stdout_success),
                     None)


def test_get_new_command(stdout, stdout_success, stderr):
    assert get_new_command(Command('pip install ipaddr', stdout=stdout,
                                   stderr=stderr), None)\
            == 'sudo pip install ipaddr'
