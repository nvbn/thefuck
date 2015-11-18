import pytest
from thefuck.rules.unknown_command import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='./bin/hdfs dfs ls', stderr='ls: Unknown command\nDid you mean -ls?  This command begins with a dash.'),
    Command(script='hdfs dfs ls',
            stderr='ls: Unknown command\nDid you mean -ls?  This command begins with a dash.'),
    Command(script='hdfs dfs ls /foo/bar', stderr='ls: Unknown command\nDid you mean -ls?  This command begins with a dash.')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='./bin/hdfs dfs -ls', stderr=''),
    Command(script='./bin/hdfs dfs -ls /foo/bar', stderr=''),
    Command(script='hdfs dfs -ls -R /foo/bar', stderr=''),
    Command()])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('hdfs dfs ls',
        stderr='ls: Unknown command\nDid you mean -ls?  This command begins with a dash.'), ['hdfs dfs -ls']),
    (Command('hdfs dfs rm /foo/bar',
        stderr='rm: Unknown command\nDid you mean -rm?  This command begins with a dash.'), ['hdfs dfs -rm /foo/bar']),
    (Command('./bin/hdfs dfs ls -R /foo/bar',
        stderr='ls: Unknown command\nDid you mean -ls?  This command begins with a dash.'), ['./bin/hdfs dfs -ls -R /foo/bar']),
    (Command('./bin/hdfs dfs -Dtest=fred ls -R /foo/bar',
        stderr='ls: Unknown command\nDid you mean -ls?  This command begins with a dash.'), ['./bin/hdfs dfs -Dtest=fred -ls -R /foo/bar'])])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
