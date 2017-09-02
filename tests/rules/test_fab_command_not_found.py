import pytest
from thefuck.rules.fab_command_not_found import match, get_new_command
from thefuck.types import Command

output = '''
Warning: Command(s) not found:
    extenson
    deloyp

Available commands:

    update_config
    prepare_extension
    Template               A string class for supporting $-substitutions.
    deploy
    glob                   Return a list of paths matching a pathname pattern.
    install_web
    set_version
'''


@pytest.mark.parametrize('command', [
    Command('fab extenson', output),
    Command('fab deloyp', output),
    Command('fab extenson deloyp', output)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('gulp extenson', output),
    Command('fab deloyp', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('script, result', [
    ('fab extenson', 'fab prepare_extension'),
    ('fab extenson:version=2016',
     'fab prepare_extension:version=2016'),
    ('fab extenson:version=2016 install_web set_version:val=0.5.0',
     'fab prepare_extension:version=2016 install_web set_version:val=0.5.0'),
    ('fab extenson:version=2016 deloyp:beta=true -H the.fuck',
     'fab prepare_extension:version=2016 deploy:beta=true -H the.fuck'),
])
def test_get_new_command(script, result):
    command = Command(script, output)
    assert get_new_command(command) == result
