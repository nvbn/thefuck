from .generic import Generic, ShellConfiguration


class Powershell(Generic):
    def app_alias(self, fuck):
        return 'function ' + fuck + ' {\n' \
               '    $history = (Get-History -Count 1).CommandLine;\n' \
               '    if (-not [string]::IsNullOrWhiteSpace($history)) {\n' \
               '        $fuck = $(thefuck $history);\n' \
               '        if (-not [string]::IsNullOrWhiteSpace($fuck)) {\n' \
               '            if ($fuck.StartsWith("echo")) { $fuck = $fuck.Substring(5); }\n' \
               '            else { iex "$fuck"; }\n' \
               '        }\n' \
               '    }\n' \
               '}\n'

    def and_(self, *commands):
        return u' -and '.join('({0})'.format(c) for c in commands)

    def how_to_configure(self):
        return ShellConfiguration(
            content=u'iex "thefuck --alias"',
            path='$profile',
            reload='& $profile',
            can_configure_automatically=False)
