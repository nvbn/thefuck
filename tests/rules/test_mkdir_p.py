import pytest
from thefuck.rules.mkdir_p import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('mkdir foo/bar/baz', 'mkdir: foo/bar: No such file or directory'),
    Command('./bin/hdfs dfs -mkdir foo/bar/baz', 'mkdir: `foo/bar/baz\': No such file or directory'),
    Command('hdfs dfs -mkdir foo/bar/baz', 'mkdir: `foo/bar/baz\': No such file or directory')
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('mkdir foo/bar/baz', ''),
    Command('mkdir foo/bar/baz', 'foo bar baz'),
    Command('hdfs dfs -mkdir foo/bar/baz', ''),
    Command('./bin/hdfs dfs -mkdir foo/bar/baz', ''),
    Command('', ''),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('mkdir foo/bar/baz', ''), 'mkdir -p foo/bar/baz'),
    (Command('hdfs dfs -mkdir foo/bar/baz', ''), 'hdfs dfs -mkdir -p foo/bar/baz'),
    (Command('./bin/hdfs dfs -mkdir foo/bar/baz', ''), './bin/hdfs dfs -mkdir -p foo/bar/baz'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
