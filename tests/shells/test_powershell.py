# -*- coding: utf-8 -*-

import pytest
from thefuck.shells import Powershell


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestPowershell(object):
    @pytest.fixture
    def shell(self):
        return Powershell()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.powershell.Popen')
        return mock

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == '(ls) -and (cd)'

    def test_app_alias(self, shell):
        assert 'function fuck' in shell.app_alias('fuck')
        assert 'function FUCK' in shell.app_alias('FUCK')
        assert 'thefuck' in shell.app_alias('fuck')

    def test_how_to_configure(self, shell):
        assert not shell.how_to_configure().can_configure_automatically

    @pytest.mark.parametrize('side_effect, expected_version, call_args', [
        ([b'''Major  Minor  Build  Revision
-----  -----  -----  --------
5      1      17763  316     \n'''], 'PowerShell 5.1.17763.316', ['powershell.exe']),
        ([IOError, b'PowerShell 6.1.2\n'], 'PowerShell 6.1.2', ['powershell.exe', 'pwsh'])])
    def test_info(self, side_effect, expected_version, call_args, shell, Popen):
        Popen.return_value.stdout.read.side_effect = side_effect
        assert shell.info() == expected_version
        assert Popen.call_count == len(call_args)
        assert all([Popen.call_args_list[i][0][0][0] == call_arg for i, call_arg in enumerate(call_args)])

    def test_get_version_error(self, shell, Popen):
        Popen.return_value.stdout.read.side_effect = RuntimeError
        with pytest.raises(RuntimeError):
            shell._get_version()
        assert Popen.call_args[0][0] == ['powershell.exe', '$PSVersionTable.PSVersion']
