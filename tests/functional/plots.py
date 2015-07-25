def with_confirmation(proc):
    """Ensures that command can be fixed when confirmation enabled."""
    proc.sendline(u'mkdir -p ~/.thefuck')
    proc.sendline(u'echo "require_confirmation = True" > ~/.thefuck/settings.py')

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    proc.expect(u'echo test')
    proc.expect(u'enter')
    proc.expect_exact(u'ctrl+c')
    proc.send('\n')

    proc.expect(u'test')


def refuse_with_confirmation(proc):
    """Ensures that fix can be refused when confirmation enabled."""
    proc.sendline(u'mkdir -p ~/.thefuck')
    proc.sendline(u'echo "require_confirmation = True" > ~/.thefuck/settings.py')

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    proc.expect(u'echo test')
    proc.expect(u'enter')
    proc.expect_exact(u'ctrl+c')
    proc.send('\003')

    proc.expect(u'Aborted')


def without_confirmation(proc):
    """Ensures that command can be fixed when confirmation disabled."""
    proc.sendline(u'mkdir -p ~/.thefuck')
    proc.sendline(u'echo "require_confirmation = False" > ~/.thefuck/settings.py')

    proc.sendline(u'ehco test')

    proc.sendline(u'fuck')
    proc.expect(u'echo test')
    proc.expect(u'test')
