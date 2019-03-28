from thefuck.rules.docker_login import match, get_new_command
from thefuck.types import Command


def test_match():
    err_response = """
    Sending build context to Docker daemon  118.8kB
Step 1/6 : FROM foo/bar:fdb7c6d
pull access denied for foo/bar, repository does not exist or may require 'docker login'
"""
    assert match(Command('docker build -t artifactory:9090/foo/bar:fdb7c6d .', err_response))
    assert not match(Command('', ''))


def test_get_new_command():
    assert get_new_command(Command('docker build -t artifactory:9090/foo/bar:fdb7c6d .', '')) == 'docker login && docker build -t artifactory:9090/foo/bar:fdb7c6d .'
