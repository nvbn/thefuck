# -*- coding: UTF-8 -*-
from thefuck.rules.pip_install import match, get_new_command
from thefuck.types import Command


def test_match():
    response1 = """
    Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Library/Python/2.7/site-packages/entrypoints.pyc'
Consider using the `--user` option or check the permissions.
"""
    assert match(Command('pip install -r requirements.txt', response1))

    response2 = """
Collecting bacon
  Downloading https://files.pythonhosted.org/packages/b2/81/19fb79139ee71c8bc4e5a444546f318e2b87253b8939ec8a7e10d63b7341/bacon-0.3.1.zip (11.0MB)
    100% |████████████████████████████████| 11.0MB 3.0MB/s
Installing collected packages: bacon
  Running setup.py install for bacon ... done
Successfully installed bacon-0.3.1
"""
    assert not match(Command('pip install bacon', response2))


def test_get_new_command():
    assert get_new_command(Command('pip install -r requirements.txt', '')) == 'pip install --user -r requirements.txt'
    assert get_new_command(Command('pip install bacon', '')) == 'pip install --user bacon'
    assert get_new_command(Command('pip install --user -r requirements.txt', '')) == 'sudo pip install -r requirements.txt'
