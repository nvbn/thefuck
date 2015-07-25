from pexpect import TIMEOUT


def with_confirmation(proc):
    """Ensures that command can be fixed when confirmation enabled."""
    proc.sendline(u'mkdir -p ~/.thefuck')
    proc.sendline(u'echo "require_confirmation = True" > ~/.thefuck/settings.py')

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'echo test'])
    assert proc.expect([TIMEOUT, u'enter'])
    assert proc.expect_exact([TIMEOUT, u'ctrl+c'])
    proc.send('\n')

    assert proc.expect([TIMEOUT, u'test'])


def refuse_with_confirmation(proc):
    """Ensures that fix can be refused when confirmation enabled."""
    proc.sendline(u'mkdir -p ~/.thefuck')
    proc.sendline(u'echo "require_confirmation = True" > ~/.thefuck/settings.py')

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'echo test'])
    assert proc.expect([TIMEOUT, u'enter'])
    assert proc.expect_exact([TIMEOUT, u'ctrl+c'])
    proc.send('\003')

    assert proc.expect([TIMEOUT, u'Aborted'])


def without_confirmation(proc):
    """Ensures that command can be fixed when confirmation disabled."""
    proc.sendline(u'mkdir -p ~/.thefuck')
    proc.sendline(u'echo "require_confirmation = False" > ~/.thefuck/settings.py')

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    assert proc.expect([TIMEOUT, u'echo test'])
    assert proc.expect([TIMEOUT, u'test'])
