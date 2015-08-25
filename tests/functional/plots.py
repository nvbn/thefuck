from pexpect import TIMEOUT


def _set_confirmation(proc, require):
    proc.sendline(u'mkdir -p ~/.thefuck')
    proc.sendline(
        u'echo "require_confirmation = {}" > ~/.thefuck/settings.py'.format(
            require))


def with_confirmation(proc):
    """Ensures that command can be fixed when confirmation enabled."""
    _set_confirmation(proc, True)

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'echo test'])
    assert proc.expect([TIMEOUT, u'enter'])
    assert proc.expect_exact([TIMEOUT, u'ctrl+c'])
    proc.send('\n')

    assert proc.expect([TIMEOUT, u'test'])


def history_changed(proc, to):
    """Ensures that history changed."""
    proc.send('\033[A')
    assert proc.expect([TIMEOUT, to])


def history_not_changed(proc):
    """Ensures that history not changed."""
    proc.send('\033[A')
    assert proc.expect([TIMEOUT, u'fuck'])


def select_command_with_arrows(proc):
    """Ensures that command can be selected with arrow keys."""
    _set_confirmation(proc, True)

    proc.sendline(u'git h')
    assert proc.expect([TIMEOUT, u"git: 'h' is not a git command."])

    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'git show'])
    proc.send('\033[B')
    assert proc.expect([TIMEOUT, u'git push'])
    proc.send('\033[B')
    assert proc.expect([TIMEOUT, u'git help'])
    proc.send('\033[A')
    assert proc.expect([TIMEOUT, u'git push'])
    proc.send('\n')

    assert proc.expect([TIMEOUT, u'Not a git repository'])


def refuse_with_confirmation(proc):
    """Ensures that fix can be refused when confirmation enabled."""
    _set_confirmation(proc, True)

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'echo test'])
    assert proc.expect([TIMEOUT, u'enter'])
    assert proc.expect_exact([TIMEOUT, u'ctrl+c'])
    proc.send('\003')

    assert proc.expect([TIMEOUT, u'Aborted'])


def without_confirmation(proc):
    """Ensures that command can be fixed when confirmation disabled."""
    _set_confirmation(proc, False)

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'echo test'])
    assert proc.expect([TIMEOUT, u'test'])
