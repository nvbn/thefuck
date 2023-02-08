def _set_confirmation(proc, require):
    proc.sendline('mkdir -p ~/.thefuck')
    proc.sendline(
        f'echo "require_confirmation = {require}" > ~/.thefuck/settings.py')


def with_confirmation(proc, TIMEOUT):
    """Ensures that command can be fixed when confirmation enabled."""
    _set_confirmation(proc, True)

    proc.sendline('ehco test')

    proc.sendline('fuck')
    assert proc.expect([TIMEOUT, 'echo test'])
    assert proc.expect([TIMEOUT, 'enter'])
    assert proc.expect_exact([TIMEOUT, 'ctrl+c'])
    proc.send('\n')

    assert proc.expect([TIMEOUT, 'test'])


def history_changed(proc, TIMEOUT, to):
    """Ensures that history changed."""
    proc.send('\033[A')
    assert proc.expect([TIMEOUT, to])


def history_not_changed(proc, TIMEOUT):
    """Ensures that history not changed."""
    proc.send('\033[A')
    assert proc.expect([TIMEOUT, 'fuck'])


def select_command_with_arrows(proc, TIMEOUT):
    """Ensures that command can be selected with arrow keys."""
    _set_confirmation(proc, True)

    proc.sendline('git h')
    assert proc.expect([TIMEOUT, "git: 'h' is not a git command."])

    proc.sendline('fuck')
    assert proc.expect([TIMEOUT, 'git show'])
    proc.send('\033[B')
    assert proc.expect([TIMEOUT, 'git push'])
    proc.send('\033[B')
    assert proc.expect([TIMEOUT, 'git help'])
    proc.send('\033[A')
    assert proc.expect([TIMEOUT, 'git push'])
    proc.send('\033[B')
    assert proc.expect([TIMEOUT, 'git help'])
    proc.send('\n')

    assert proc.expect([TIMEOUT, 'usage'])


def refuse_with_confirmation(proc, TIMEOUT):
    """Ensures that fix can be refused when confirmation enabled."""
    _set_confirmation(proc, True)

    proc.sendline('ehco test')

    proc.sendline('fuck')
    assert proc.expect([TIMEOUT, 'echo test'])
    assert proc.expect([TIMEOUT, 'enter'])
    assert proc.expect_exact([TIMEOUT, 'ctrl+c'])
    proc.send('\003')

    assert proc.expect([TIMEOUT, 'Aborted'])


def without_confirmation(proc, TIMEOUT):
    """Ensures that command can be fixed when confirmation disabled."""
    _set_confirmation(proc, False)

    proc.sendline('ehco test')

    proc.sendline('fuck')
    assert proc.expect([TIMEOUT, 'echo test'])
    assert proc.expect([TIMEOUT, 'test'])


def how_to_configure(proc, TIMEOUT):
    proc.sendline('fuck')
    assert proc.expect([TIMEOUT, "alias isn't configured"])
