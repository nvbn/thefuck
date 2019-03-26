import pytest
from thefuck.rules.bc import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('script, output', [
    ('cb', 'bash: command not found: cb'),
    ('bv', 'bash: command not found: bv'),
    ('bb', 'bash: command not found: bb'),
    ('vc 12', 'bash: command not found: vb'),
    ])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', [
    'cb'
    'vc file'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, output', [
    ('vc', 'bc'),
    ('bv file', 'bc file')])
def test_get_new_command(script, output):
    assert get_new_command(Command(script, '')) == output