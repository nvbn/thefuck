def with_confirmation(proc):
    """Ensures that command can be fixed when confirmation enabled."""
    proc.sendline('mkdir -p ~/.thefuck')
    proc.sendline('echo "require_confirmation = True" > ~/.thefuck/settings.py')

    proc.sendline('ehco test')

    proc.sendline('fuck')
    proc.expect('echo test')
    proc.expect('enter')
    proc.expect_exact('ctrl+c')
    proc.send('\n')

    proc.expect('test')


def refuse_with_confirmation(proc):
    """Ensures that fix can be refused when confirmation enabled."""
    proc.sendline('mkdir -p ~/.thefuck')
    proc.sendline('echo "require_confirmation = True" > ~/.thefuck/settings.py')

    proc.sendline('ehco test')

    proc.sendline('fuck')
    proc.expect('echo test')
    proc.expect('enter')
    proc.expect_exact('ctrl+c')
    proc.send('\003')

    proc.expect('Aborted')


def without_confirmation(proc):
    """Ensures that command can be fixed when confirmation disabled."""
    proc.sendline('mkdir -p ~/.thefuck')
    proc.sendline('echo "require_confirmation = False" > ~/.thefuck/settings.py')

    proc.sendline('ehco test')

    proc.sendline('fuck')
    proc.expect('echo test')
    proc.expect('test')
