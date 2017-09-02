import pytest
from thefuck.rules.rm_dir import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('rm foo', 'rm: foo: is a directory'),
    Command('rm foo', 'rm: foo: Is a directory'),
    Command('hdfs dfs -rm foo', 'rm: `foo`: Is a directory'),
    Command('./bin/hdfs dfs -rm foo', 'rm: `foo`: Is a directory'),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('rm foo', ''),
    Command('hdfs dfs -rm foo', ''),
    Command('./bin/hdfs dfs -rm foo', ''),
    Command('', ''),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('rm foo', ''), 'rm -rf foo'),
    (Command('hdfs dfs -rm foo', ''), 'hdfs dfs -rm -r foo'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
