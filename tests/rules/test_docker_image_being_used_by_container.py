from thefuck.rules.docker_image_being_used_by_container import match, get_new_command
from thefuck.types import Command


def test_match():
    err_response = """Error response from daemon: conflict: unable to delete cd809b04b6ff (cannot be forced) - image is being used by running container e5e2591040d1"""
    assert match(Command('docker image rm -f cd809b04b6ff', err_response))


def test_not_match():
    err_response = 'bash: docker: command not found'
    assert not match(Command('docker image rm -f cd809b04b6ff', err_response))


def test_not_docker_command():
    err_response = """Error response from daemon: conflict: unable to delete cd809b04b6ff (cannot be forced) - image is being used by running container e5e2591040d1"""
    assert not match(Command('git image rm -f cd809b04b6ff', err_response))


def test_get_new_command():
    err_response = """
        Error response from daemon: conflict: unable to delete cd809b04b6ff (cannot be forced) - image
        is being used by running container e5e2591040d1
        """
    result = get_new_command(Command('docker image rm -f cd809b04b6ff', err_response))
    expected = 'docker container rm -f e5e2591040d1 && docker image rm -f cd809b04b6ff'
    assert result == expected
