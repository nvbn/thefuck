import pytest
from thefuck.rules.choco_install import get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('before, after', [
    ('choco install logstitcher', 'choco install logstitcher.install'),
    ('cinst logstitcher', 'cinst logstitcher.install'),
    ('choco install logstitcher -y', 'choco install logstitcher.install -y'),
    ('cinst logstitcher -y', 'cinst logstitcher.install -y')])
def test_get_new_command(before, after):
    assert (get_new_command(Command(before, '')) == after)
