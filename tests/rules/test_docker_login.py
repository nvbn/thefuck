from thefuck.rules.docker_login import match, get_new_command
from thefuck.types import Command


def test_match():
    err_response1 = """
    Sending build context to Docker daemon  118.8kB
Step 1/6 : FROM foo/bar:fdb7c6d
pull access denied for foo/bar, repository does not exist or may require 'docker login'
"""
    assert match(Command('docker build -t artifactory:9090/foo/bar:fdb7c6d .', err_response1))

    err_response2 = """
    The push refers to repository [artifactory:9090/foo/bar]
push access denied for foo/bar, repository does not exist or may require 'docker login'
"""
    assert match(Command('docker push artifactory:9090/foo/bar:fdb7c6d', err_response2))

    err_response3 = """
    docker push artifactory:9090/foo/bar:fdb7c6d
The push refers to repository [artifactory:9090/foo/bar]
9c29c7ad209d: Preparing
71f3ad53dfe0: Preparing
f58ee068224c: Preparing
aeddc924d0f7: Preparing
c2040e5d6363: Preparing
4d42df4f350f: Preparing
35723dab26f9: Preparing
71f3ad53dfe0: Pushed
cb95fa0faeb1: Layer already exists
"""
    assert not match(Command('docker push artifactory:9090/foo/bar:fdb7c6d', err_response3))


def test_get_new_command():
    assert get_new_command(Command('docker build -t artifactory:9090/foo/bar:fdb7c6d .', '')) == 'docker login && docker build -t artifactory:9090/foo/bar:fdb7c6d .'
    assert get_new_command(Command('docker push artifactory:9090/foo/bar:fdb7c6d', '')) == 'docker login && docker push artifactory:9090/foo/bar:fdb7c6d'
