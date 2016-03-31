import os
import pytest
from thefuck.rules.ssh_known_hosts import match, get_new_command,\
    side_effect
from tests.utils import Command


@pytest.fixture
def ssh_error(tmpdir):
    path = os.path.join(str(tmpdir), 'known_hosts')

    def reset(path):
        with open(path, 'w') as fh:
            lines = [
                '123.234.567.890 asdjkasjdakjsd\n'
                '98.765.432.321 ejioweojwejrosj\n'
                '111.222.333.444 qwepoiwqepoiss\n'
            ]
            fh.writelines(lines)

    def known_hosts(path):
        with open(path, 'r') as fh:
            return fh.readlines()

    reset(path)

    errormsg = u"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
b6:cb:07:34:c0:a0:94:d3:0d:69:83:31:f4:c5:20:9b.
Please contact your system administrator.
Add correct host key in {0} to get rid of this message.
Offending RSA key in {0}:2
RSA host key for {1} has changed and you have requested strict checking.
Host key verification failed.""".format(path, '98.765.432.321')

    return errormsg, path, reset, known_hosts


def test_match(ssh_error):
    errormsg, _, _, _ = ssh_error
    assert match(Command('ssh', stderr=errormsg))
    assert match(Command('ssh', stderr=errormsg))
    assert match(Command('scp something something', stderr=errormsg))
    assert match(Command('scp something something', stderr=errormsg))
    assert not match(Command(stderr=errormsg))
    assert not match(Command('notssh', stderr=errormsg))
    assert not match(Command('ssh'))


@pytest.mark.skipif(os.name == 'nt', reason='Skip if testing on Windows')
def test_side_effect(ssh_error):
    errormsg, path, reset, known_hosts = ssh_error
    command = Command('ssh user@host', stderr=errormsg)
    side_effect(command, None)
    expected = ['123.234.567.890 asdjkasjdakjsd\n', '111.222.333.444 qwepoiwqepoiss\n']
    assert known_hosts(path) == expected


def test_get_new_command(ssh_error, monkeypatch):
    errormsg, _, _, _ = ssh_error
    assert get_new_command(Command('ssh user@host', stderr=errormsg)) == 'ssh user@host'
