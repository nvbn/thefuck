def with_confirmation(proc):
    """Ensures that command can be fixed when confirmation enabled."""
    proc.sendline('ehco test')

    proc.sendline('fuck')
    proc.expect('echo test')
    proc.expect('enter')
    proc.expect_exact('ctrl+c')
    proc.send('\n')

    proc.expect('test')


def without_confirmation(proc):
    """Ensures that command can be fixed when confirmation disabled."""
    proc.sendline('ehco test')

    proc.sendline('fuck')
    proc.expect('echo test')
    proc.expect('test')
