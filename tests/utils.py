from thefuck import types


def Command(script='', stdout='', stderr=''):
    return types.Command(script, stdout, stderr)


def Rule(name='', match=lambda *_: True,
         get_new_command=lambda *_: '',
         enabled_by_default=True):
    return types.Rule(name, match, get_new_command, enabled_by_default)
