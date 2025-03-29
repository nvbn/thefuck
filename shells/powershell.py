from subprocess import Popen, PIPE
from ..utils import DEVNULL
from .generic import Generic, ShellConfiguration


class Powershell(Generic):
    friendly_name = 'PowerShell'

    def app_alias(self, alias_name):
        return 'function ' + alias_name + ' {\n' \
               '    $history = (Get-History -Count 1).CommandLine;\n' \
               '    if (-not [string]::IsNullOrWhiteSpace($history)) {\n' \
               '        $fuck = $(thefuck $args $history);\n' \
               '        if (-not [string]::IsNullOrWhiteSpace($fuck)) {\n' \
               '            if ($fuck.StartsWith("echo")) { $fuck = $fuck.Substring(5); }\n' \
               '            else { iex "$fuck"; }\n' \
               '        }\n' \
               '    }\n' \
               '    [Console]::ResetColor() \n' \
               '}\n'

    def and_(self, *commands):
        return u' -and '.join('({0})'.format(c) for c in commands)

    def how_to_configure(self):
        return ShellConfiguration(
            content=u'iex "$(thefuck --alias)"',
            path='$profile',
            reload='. $profile',
            can_configure_automatically=False)

    def _get_version(self):
        """Returns the version of the current shell"""
        try:
            proc = Popen(
                ['powershell.exe', '$PSVersionTable.PSVersion'],
                stdout=PIPE,
                stderr=DEVNULL)
            version = proc.stdout.read().decode('utf-8').rstrip().split('\n')
            return '.'.join(version[-1].split())
        except IOError:
            proc = Popen(['pwsh', '--version'], stdout=PIPE, stderr=DEVNULL)
            return proc.stdout.read().decode('utf-8').split()[-1]
