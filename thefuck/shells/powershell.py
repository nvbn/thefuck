from .generic import Generic


class Powershell(Generic):
    def app_alias(self, fuck):
        return 'function ' + fuck + ' { \n' \
               '    $fuck = $(thefuck (Get-History -Count 1).CommandLine);\n' \
               '    if (-not [string]::IsNullOrWhiteSpace($fuck)) {\n' \
               '        if ($fuck.StartsWith("echo")) { $fuck = $fuck.Substring(5); }\n' \
               '        else { iex "$fuck"; }\n' \
               '    }\n' \
               '}\n'

    def and_(self, *commands):
        return u' -and '.join('({0})'.format(c) for c in commands)

    def how_to_configure(self):
        return {
            'content': 'iex "thefuck --alias"',
            'path': '$profile',
            'reload': '& $profile',
        }
